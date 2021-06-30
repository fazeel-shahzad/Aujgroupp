from odoo import api,fields,models,_

import logging
_logger = logging.getLogger(__name__)








class SalesOrderTaxReport(models.AbstractModel):
    _name = 'report.so_tax_invoice.saleorder_tax_report'
     
    @api.model
    def _get_report_values(self, docids, data=None):
        try:
            sale_order_recs = self.env["sale.order"].search([("id","in",docids)])

#              model = self.env.context.get('active_model')
#              docs = self.env[model].browse(self.env.context.get('active_id'))

            return {
                'so':sale_order_recs,

                }
         
        except Exception as e:
            _logger.exception(e)
            print(e)