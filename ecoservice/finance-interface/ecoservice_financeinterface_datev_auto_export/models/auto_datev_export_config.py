# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files in the root directory of this module for full details.

# Standard
from datetime import datetime, timedelta

# 3rd
from dateutil.relativedelta import relativedelta

# Odoo
from odoo import fields, models
from odoo.exceptions import UserError


class AutoDatevExportConfig(models.Model):
    _name = 'auto.datev.export.config'
    _description = 'Auto Datev Export Config'
    _rec_name = 'partner_id'

    # region Fields

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
    )

    period = fields.Selection(
        selection=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
        ],
    )

    # endregion

    # region Constraints

    _sql_constraints = [
        (
            'partner_period_unique',
            'unique (partner_id, period)',
            'A period could be defined only one time for same partner.',
        )
    ]

    # endregion

    def auto_mail_send(self):
        self.auto_send_mail_daily()
        self.auto_send_mail_weekly()
        self.auto_send_mail_monthly()

    def auto_send_mail_daily(self):
        configs = self.env.user.company_id.auto_datev_export_config_ids
        configs_daily = configs.filtered(lambda a: a.period == 'daily')
        if configs_daily:
            start_date = datetime.today().date()
            end_date = datetime.today().date()
            ecofi = self.generate_financial_report_csv(start_date, end_date)
            if ecofi:
                self.send_mail_to_partners(configs_daily, ecofi)

    def auto_send_mail_weekly(self):
        configs = self.env.user.company_id.auto_datev_export_config_ids
        configs_weekly = configs.filtered(lambda a: a.period == 'weekly')
        if configs_weekly:
            if datetime.today().strftime('%A') == 'Monday':
                start_date = fields.Datetime.now() - timedelta(days=7)
                end_date = datetime.today().date()
                ecofi = self.generate_financial_report_csv(start_date, end_date)
                if ecofi:
                    self.send_mail_to_partners(configs_weekly, ecofi)

    def auto_send_mail_monthly(self):
        configs = self.env.user.company_id.auto_datev_export_config_ids
        configs_monthly = configs.filtered(lambda a: a.period == 'monthly')
        if configs_monthly:
            if datetime.today().strftime('%d') == '01':
                start_date = (fields.Datetime.now() + relativedelta(months=-1)).date()
                end_date = datetime.today().date()
                ecofi = self.generate_financial_report_csv(start_date, end_date)
                if ecofi:
                    self.send_mail_to_partners(configs_monthly, ecofi)

    def generate_financial_report_csv(self, start_date, end_date):
        journals = self.env.user.company_id.journal_ids
        try:
            ecofi = self.env['ecofi'].search([
                ('date_from', '=', start_date),
                ('date_to', '=', end_date),
            ])
            if ecofi:
                return ecofi
            else:
                return self.env['ecofi'].ecofi_buchungen(journals, start_date, end_date)
        except UserError:
            return False

    def send_mail_to_partners(self, configs, ecofi):
        template_id = self.env['ir.model.data'].get_object_reference(
            'ecoservice_financeinterface_datev_auto_export',
            'send_email_finance_report_summary',
        )[1]
        for config in configs:
            if config.partner_id != self.env.user:
                template = self.env['mail.template'].browse(template_id)
                if template:
                    attachment = self.create_attachment(ecofi)

                    values = template.generate_email(config.id, fields=None)
                    values.update({
                        'subject': ' '.join([
                            'Financial Summary Report From',
                            ecofi.date_from.strftime('%d-%m-%Y'),
                            'To',
                            ecofi.date_to.strftime('%d-%m-%Y'),
                        ]),
                        'email_from': self.env.user.email,
                        'email_to': config.partner_id.email,
                        'recipient_ids': False,
                        'message_type': 'email',
                        'res_id': False,
                        'reply_to': False,
                        'author_id': self.env.user.partner_id.id,
                        'attachment_ids': [(6, 0, attachment.ids)],
                    })

                    mail = self.env['mail.mail'].sudo().create(values)
                    if mail:
                        mail.send()

    def create_attachment(self, ecofi):
        return self.env['ir.attachment'].sudo().create({
            'datas': ecofi.csv_file,
            'name': ecofi.name + '.csv',
            'type': 'binary',
            'store_fname': ecofi.csv_file,
            'res_model': 'ecofi',
        })
