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
  "name"                 :  "Discount On Sale Order",
  "summary"              :  """The module allows you to set discount in fixed/percent basis for orders and order lines separately. The total discount in an order is sum of global discount and order line discount.""",
  "category"             :  "Sales",
  "version"              :  "2.2.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Discount-On-Sale-Order.html",
  "description"          :  """Odoo Discount On Sale Order
Order line discount
Odoo discount
Order discount
Fixed order line discount
Percentage discount odoo
Customer discount
Purchase discount
Sales order discount
Discount per product""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=discount_sale_order",
  "depends"              :  [
                             'sale_management',
                             'discount_account_invoice',
                            ],
  "data"                 :  [
                             'views/sale_views.xml',
                             'views/sale_portal_templates.xml',
                             'report/sale_report_templates.xml',
                            ],
  "demo"                 :  ['data/discount_demo.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  55,
  "currency"             :  "USD",
  "pre_init_hook"        :  "pre_init_check",
}