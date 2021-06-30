# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files in the root directory of this module for full details.

from odoo import fields, models


class DatevReferenceDataExport(models.TransientModel):
    _name = 'datev.reference.data.export'

    # region Fields

    export_format_id = fields.Many2one(
        comodel_name='ecofi.datev.formate',
        string='Export Format',
        required=True,
    )
    file_export = fields.Binary(string='Export File')
    file_export_name = fields.Char(string='Export Filename')
    file_export_log = fields.Text(
        string='Export Log',
        readonly=True,
    )

    # endregion

    def startexport(self):
        """
        Start the export through the wizard.
        """
        for export in self:
            export_file = export.export_format_id.generate_export()
            filename = '{name}_{date}.csv'.format(
                name=export.export_format_id.name,
                date=fields.Datetime.now().strftime('%y%m%d'),
            )
            export.write({
                'file_export': export_file['file'],
                'file_export_log': export_file['log'],
                'file_export_name': filename,
            })

        view_id = self.env.ref(
            'ecoservice_financeinterface_master_data.datev_export_view'
        )

        return {
            'res_id': self.id,
            'view_id': [view_id.id],
            'view_mode': 'form',
            'res_model': 'datev.reference.data.export',
            'type': 'ir.actions.act_window',
            'context': {'step': 'just_anonymized'},
            'target': 'new',
        }
