# Part of AktivSoftware
# See LICENSE file for full copyright and licensing details.


from odoo import models


class MailComposer(models.TransientModel):
    """When email is sent from Quotation.

    We will prevent to add customer as Follower in Quotation.
    """

    _inherit = 'mail.compose.message'

    def send_mail(self, auto_commit=False):
        """
        Unlink follower if active model is SO.

        :param auto_commit: Base

        :return: super
        """

        res = super(MailComposer, self).send_mail(auto_commit)
        if self._context.get('active_model') == 'sale.order':
            order = self.env['sale.order'].browse(
                self._context.get('active_id'))
            follower = order.message_follower_ids.filtered(
                lambda m: m.partner_id == order.partner_id
            )
            if follower:
                follower.unlink()
        return res
