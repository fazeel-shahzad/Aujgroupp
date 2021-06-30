from odoo import api,fields,models,_

import logging
_logger = logging.getLogger(__name__)








class SalesTaxInvoiceReport(models.AbstractModel):
    _name = 'report.sales_tax_invoice.invoice_tax_report'
     
    @api.model
    def _get_report_values(self, docids, data=None):
        try:
            acct_invoice = self.env["account.move"].search([("id","in",docids)])

#              model = self.env.context.get('active_model')
#              docs = self.env[model].browse(self.env.context.get('active_id'))

            return {
                'account':acct_invoice,

                }
         
        except Exception as e:
            _logger.exception(e)
            print(e)