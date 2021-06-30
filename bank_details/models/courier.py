from odoo import models


class PartnerCourierXlsx(models.AbstractModel):
    _name = 'report.bank_details.report_courier_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, vendors):
        format0 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        format1 = workbook.add_format({'font_size': 11, 'align': 'vcenter', 'bold': True})
        format2 = workbook.add_format({'font_size': 8, 'align': 'vcenter', })
        sheet = workbook.add_worksheet('Student Data Card')
        i = 0
        for rec in vendors:
            sheet.write(i + 1, 3, 'Couriers', format0)
            sheet.write(i + 3, 2, 'Company Name', format1)
            sheet.write(i + 3, 3, rec.name, format2)
            # sheet.write(i+3, 4, rec.currency_id.name, format1)
            sheet.write(i + 4, 2, 'Address', format1)
            sheet.write(i + 4, 3, rec.street + rec.city if rec.city else '' + rec.country_id if rec.country_id else '', format2)
            sheet.write(i + 5, 2, 'Contact Person', format1)
            sheet.write(i + 5, 3, rec.child_ids[0].name if rec.child_ids else '', format2)
            i = i + 7


