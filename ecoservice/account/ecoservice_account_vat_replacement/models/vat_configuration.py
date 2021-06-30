# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from odoo import fields, models


class VatConfiguration(models.Model):
    _name = 'vat.configuration'
    _description = 'VAT Configuration'
    _rec_name = 'description'

    # region Fields
    description = fields.Char(
        required=True,
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        required=True,
    )
    execution_time = fields.Datetime()
    scheduled_cron_job = fields.Many2one(
        comodel_name='ir.cron',
    )
    cron_nextcall = fields.Datetime(
        related='scheduled_cron_job.nextcall',
    )
    cron_active = fields.Boolean(
        related='scheduled_cron_job.active',
    )

    configuration_account_ids = fields.One2many(
        comodel_name='vat.configuration.account',
        inverse_name='configuration_id',
    )
    configuration_tax_ids = fields.One2many(
        comodel_name='vat.configuration.tax',
        inverse_name='configuration_id',
    )
    # endregion

    # region CRUD Methods
    def unlink(self):
        self.with_context(active_test=False).sudo().scheduled_cron_job.unlink()
        return super().unlink()

    # endregion

    # region Action Methods
    def action_run(self):
        self.run()

    def action_cron(self):
        vals = self.create_cron_vals()
        if self.scheduled_cron_job:
            self.scheduled_cron_job.sudo().write(vals)
        else:
            cron_rec = self.env['ir.cron'].sudo().create(vals)
            self.write({'scheduled_cron_job': cron_rec.id})
            self.create_xmlid(cron_rec)

    # endregion

    # region Business Methods
    def run(self):
        for configuration in self:
            configuration.run_account_replacement()
            configuration.run_tax_replacement()

    def run_account_replacement(self):
        for line in self.configuration_account_ids:
            self._replace_account_in_product(
                line.source_account_id,
                line.target_account_id,
            )
            self._replace_account_in_category(
                line.source_account_id,
                line.target_account_id,
            )

    def run_tax_replacement(self):
        for line in self.configuration_tax_ids:
            self._replace_tax_in_product(
                line.source_tax_id,
                line.target_tax_id,
            )

    def _replace_account_in_product(self, source, target):
        for field in ['property_account_income_id', 'property_account_expense_id']:
            self.env['product.product'].sudo().with_context(
                force_company=self.company_id.id,
            ).search([
                (field, '=', source.id),
            ]).write({
                field: target.id,
            })

    def _replace_account_in_category(self, source, target):
        for field in [
            'property_account_income_categ_id',
            'property_account_expense_categ_id',
        ]:
            self.env['product.category'].sudo().with_context(
                force_company=self.company_id.id,
            ).search([
                (field, '=', source.id),
            ]).write({
                field: target.id,
            })

    def _replace_tax_in_product(self, source, target):
        for field in ['taxes_id', 'supplier_taxes_id']:
            self.env['product.product'].sudo().with_context(
                force_company=self.company_id.id,
            ).search([
                (field, '=', source.id),
            ]).write({
                field: [
                    (3, source.id),
                    (4, target.id),
                ],
            })

    def create_cron_vals(self):

        name = 'schedule_replace_account_tax_{conf_id}'.format(conf_id=self.id)
        vat_model = self.env.ref(
            'ecoservice_account_vat_replacement.model_vat_configuration',
        )
        code = 'model.browse({conf_id}).run()'.format(conf_id=self.id)

        vals = {
            'name': name,
            'model_id': vat_model.id,
            'numbercall': 1,
            'nextcall': self.execution_time,
            'code': code,
        }
        return vals

    def create_xmlid(self, cronjob):
        vals = {
            'module': 'ecoservice_account_vat_replacement',
            'name': cronjob.name,
            'model': 'ir.cron',
            'res_id': cronjob.id,
            'noupdate': True,
        }
        self.env['ir.model.data'].create(vals)

    # endregion
