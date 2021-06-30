from odoo import models


class PartnerXlsx(models.AbstractModel):
    _name = 'report.bank_details.report_bank_details_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, vendors):
        format0 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        format1 = workbook.add_format({'font_size': 11, 'align': 'vcenter', 'bold': True})
        format2 = workbook.add_format({'font_size': 8, 'align': 'vcenter', })
        sheet = workbook.add_worksheet('Student Data Card')
        i = 0
        for rec in vendors:
            sheet.write(i+1, 4, 'Bank Details', format0)
            sheet.write(i+3, 2, 'Beneficiary Name', format1)
            sheet.write(i+3, 3, rec.beneficiary_name, format2)
            sheet.write(i+3, 4, rec.currency_id.name, format1)
            sheet.write(i+4, 2, 'Bank Name', format1)
            sheet.write(i+4, 3, rec.bank_name, format2)
            sheet.write(i+5, 2, 'Address', format1)
            sheet.write(i+5, 3, rec.address, format2)
            sheet.write(i+6, 2, 'IBAN No', format1)
            sheet.write(i+6, 3, rec.iban_no, format2)
            sheet.write(i+7, 2, 'Swift Code', format1)
            sheet.write(i+7, 3, rec.swift_code, format2)
            sheet.write(i+8, 2, 'Account No', format1)
            sheet.write(i+8, 3, rec.ac_no, format2)
            sheet.write(i+9, 2, 'Short Code', format1)
            sheet.write(i+9, 3, rec.short_code, format2)
            sheet.write(i+10, 2, 'Purpose', format1)
            sheet.write(i+10, 3, rec.purpose, format2)
            i = i + 12


