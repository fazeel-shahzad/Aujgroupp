# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files in the root directory of this module for full details.

from odoo import fields, models


class EcofiDatevSpalten(models.Model):
    _name = 'ecofi.datev.spalten'
    _description = 'Configuration for Datev Reference Data Exports Columns'
    _order = 'datevid asc'

    # region Fields

    datevid = fields.Integer(
        string='Datev ID',
        readonly=True,
    )
    feldname = fields.Char(
        string='Fieldname',
        readonly=True,
    )
    typ = fields.Char(
        string='Fieldtype',
        readonly=True,
    )
    laenge = fields.Integer(
        string='Length',
        readonly=True,
    )
    nks = fields.Integer(
        string='Decimal places',
        readonly=True,
    )
    maxlaenge = fields.Integer(
        string='Maximal length',
        readonly=True,
    )
    mussfeld = fields.Boolean(
        string='Mandatory field',
        readonly=True,
    )
    beschreibung = fields.Text(
        string='Description',
        readonly=True,
    )
    import_id = fields.Many2one(
        comodel_name='ecofi.datev.formate',
        string='Import',
        required=True,
        ondelete='cascade',
        index=True,
    )
    mako = fields.Text()

    # endregion
