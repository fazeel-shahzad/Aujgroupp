# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    # region Fields
    ecofi_validations_enabled = fields.Boolean(
        string='Enabled Validations',
        default=True,
    )
    ecofi_validation_id = fields.Many2one(
        comodel_name='ecofi.validation',
        compute='_compute_ecofi_validation_id',
        store=True,
        ondelete='cascade',
        readonly=1,
        copy=False,
    )
    journal_ids = fields.Many2many(
        comodel_name='account.journal',
        relation='res_company_account_journal',
        column1='res_company_id',
        column2='account_journal_id',
        string='Default Journals',
        check_company=True,
    )
    # endregion

    # region Business Methods
    def uses_skr(self):
        return self.sudo().chart_template_id.name in [
            'Deutscher Kontenplan SKR03',
            'Deutscher Kontenplan SKR04',
        ]
    # endregion

    def _compute_ecofi_validation_id(self):
        ev = self.sudo().env['ecofi.validation']
        for rec in self:
            if rec.id:  # Avoid NewId
                rec.ecofi_validation_id = (
                    ev.search([
                        ('company_id', '=', rec.id)
                    ])
                    or ev.create({
                        'company_id': rec.id
                    })
                )

    @api.model
    def create(self, vals):
        res = super(ResCompany, self).create(vals)
        model_ecofi = self.env['ecofi.validation'].sudo()
        res.ecofi_validation_id = model_ecofi.create({
            'company_id': res.id,
        })
        return res
