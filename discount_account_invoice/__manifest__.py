# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "Discounts On Invoices And Bills",
  "summary"              :  """Discount on invoice/bill lines and invoices/bills along with fixed and percentage discount""",
  "category"             :  "Accounting",
  "version"              :  "1.1.1",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Discounts-On-Invoices-Bills.html",
  "description"          :  """Odoo Discount On Sale Order
Odoo Discount on Purchase Order
Odoo Discount on Invoices
Odoo Discount on Bills
Sales order discount
Purchase order discount
Invoice discount
Bill discount
PO discount
Vendor discount Odoo
Odoo vendor discount
Instant discount Odoo
Order line discount
Odoo discount
Fixed discount
Percentage discount odoo
Customer discount
Purchase discount
Discount per product""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=discount_account_invoice",
  "depends"              :  ['account'],
  "data"                 :  [
                             'security/security.xml',
                             'views/res_config_settings_view.xml',
                             'views/account_move_view.xml',
                             'report/report_invoice.xml',
                            ],
  "demo"                 :  ['data/discount_demo.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  25,
  "currency"             :  "USD",
  "pre_init_hook"        :  "pre_init_check",
}