# Part of AktivSoftware
# See LICENSE file for full copyright and licensing details.

from odoo import _, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    """When Quotation is conformed.

    We will prevent to add customer as Follower in Quotation
    """

    _inherit = 'sale.order'

    def action_confirm(self):
        """
        Prevent message_subscribe for customer.

        :return: True
        """

        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the '
                'following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))
        # for order in self.filtered(
        # lambda order: order.partner_id not in order.message_partner_ids):
        #     order.message_subscribe([order.partner_id.id])
        self.write({
            'state': 'sale',
            'date_order': fields.Datetime.now()
        })
        self._action_confirm()
        if self.env.user.has_group('sale.group_auto_done_setting'):
            self.action_done()
        return True
