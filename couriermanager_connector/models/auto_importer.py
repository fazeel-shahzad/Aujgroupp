from odoo import models, fields, api, _
from odoo.osv import osv
import requests
import json
import datetime


class CourierManagerAutoConnector(models.Model):
    _name = 'couriermanager.autoconnector'

    field_name = fields.Char('couriermanager_autoconnector')
    expedition_info_start_number = fields.Integer("Starting Number")
    auto_import_expedition_price = fields.Boolean("Shipping Price")
    auto_import_expedition_info = fields.Boolean("Shipping Info")
    auto_import_routing_cities = fields.Boolean("Routing Cities")
    auto_import_invoices = fields.Boolean("Invoices")
    interval_number_expedition_price = fields.Integer(string="Sync Interval Unit")
    interval_unit_expedition_price = fields.Selection([
        ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('work_days', 'Work Days'),
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months'),
    ], string='Interval Unit')
    interval_number_expedition_info = fields.Integer(string="Sync Interval Unit")
    interval_unit_expedition_info = fields.Selection([
        ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('work_days', 'Work Days'),
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months'),
    ], string='Interval Unit')
    interval_number_routing_cities = fields.Integer(string="Sync Interval Unit")
    interval_unit_routing_cities = fields.Selection([
        ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('work_days', 'Work Days'),
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months'),
    ], string='Interval Unit')
    interval_number_invoices = fields.Integer(string="Sync Interval Unit")
    interval_unit_invoices = fields.Selection([
        ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('work_days', 'Work Days'),
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months'),
    ], string='Interval Unit')

    def sync_data(self):
        """
        Automatically syncing data (shipment price, info , routing cities and invoices) between odoo and couriermanager
        """
        done = False
        while not done:
            try:
                scheduler = self.env['ir.cron'].search([('name', '=', 'Shipment Info Scheduler')])
                if not scheduler:
                    scheduler = self.env['ir.cron'].search([('name', '=', 'Shipment Info Scheduler'),
                                                            ('active', '=', False)])
                scheduler.active = self.auto_import_expedition_info
                scheduler.interval_number = self.interval_number_expedition_info
                scheduler.interval_type = self.interval_unit_expedition_info

                scheduler = self.env['ir.cron'].search([('name', '=', 'Shipment Price Scheduler')])
                if not scheduler:
                    scheduler = self.env['ir.cron'].search([('name', '=', 'Shipment Price Scheduler'),
                                                            ('active', '=', False)])
                scheduler.active = self.auto_import_expedition_price
                scheduler.interval_number = self.interval_number_expedition_price
                scheduler.interval_type = self.interval_unit_expedition_price

                scheduler = self.env['ir.cron'].search([('name', '=', 'Routing Cities Scheduler')])
                if not scheduler:
                    scheduler = self.env['ir.cron'].search([('name', '=', 'Routing Cities Scheduler'),
                                                            ('active', '=', False)])
                scheduler.active = self.auto_import_routing_cities
                scheduler.interval_number = self.interval_number_routing_cities
                scheduler.interval_type = self.interval_unit_routing_cities

                scheduler = self.env['ir.cron'].search([('name', '=', 'Invoices Scheduler')])
                if not scheduler:
                    scheduler = self.env['ir.cron'].search([('name', '=', 'Invoices Scheduler'),
                                                            ('active', '=', False)])
                scheduler.active = self.auto_import_invoices
                scheduler.interval_number = self.interval_number_invoices
                scheduler.interval_type = self.interval_unit_invoices

                self.env.cr.commit()
                done = True
            except Exception as e:
                print(str(e))

    def auto_import_ex_price(self):
        try:
            clients = self.env['couriermanager.connector'].search([('state', '=', 'connected')])
            for client in clients:
                if client.api_key:
                    baseURL = 'http://app.curiermanager.ro/cscourier/API/'
                    expedition_price_url = baseURL + 'get_price?api_key=' + str(client.api_key)
                    headers = {
                        'Accept': 'application/json',
                        'connection': 'keep-Alive'
                    }
                    response = requests.get(url=expedition_price_url, headers=headers)
                    if response.status_code == 200:
                        expedition_prices = json.loads(response.content.decode('utf-8'))['data']

                        odoo_ex_price = self.env['expedition.price'].search(
                            [('cm_client_name', '=', client.name),
                             ('cm_expedition_price', '=', expedition_prices['price']),
                             ('cm_expedition_zone', '=', expedition_prices['zone'])])
                        if not odoo_ex_price:
                            self.env['expedition.price'].create({
                                'cm_client_name': client.name,
                                'cm_expedition_price': expedition_prices['price'],
                                'cm_expedition_zone': expedition_prices['zone'],
                            })
                        self.env.cr.commit()
                    else:
                        raise osv.except_osv('', 'While importing expedition prices something went wrong please '
                                                 'try again or check API key.')

        except Exception as e:
            Warning(_(str(e)))

    def auto_import_ex_info(self):
        try:
            clients = self.env['couriermanager.connector'].search([('state', '=', 'connected')])
            started_from = 0
            expedition_numbers = self.env['expedition.info'].search([])
            if len(expedition_numbers) > 0:
                int_numbers = [int(number.ex_number) for number in expedition_numbers]
                started_from = max(int_numbers)
            else:
                started_from = self.env['couriermanager.autoconnector'].search([]).expedition_info_start_number
            for client in clients:
                if client.api_key:
                    baseURL = 'http://app.curiermanager.ro/cscourier/API/'
                    awb_url = baseURL + 'get_info?api_key=' + str(client.api_key)
                    awb_url_extend = awb_url + '&awbno='
                    headers = {
                        'Accept': 'application/json',
                        'connection': 'keep-Alive'
                    }
                    end_to = started_from + 100
                    break_here = started_from
                    while break_here <= end_to:
                        response = requests.get(url=awb_url_extend + str(break_here), headers=headers)
                        testing_response = requests.get(url=awb_url_extend + str(break_here), headers=headers)
                        if testing_response.status_code == 200:
                            break_here += 1
                            shipment = json.loads(testing_response.content.decode('utf-8'))['data']
                            kpoi=shipment['no']+"+"+shipment['status']+"+"+client.name

                            if shipment['status'] == '' and shipment['info']['price'] == 0.0 and shipment['info']['ramburs'] == '':
                                continue
                            if shipment['status'] == 'delivered':
                                print(kpoi)


                                awb_date_url = baseURL + 'get_history?api_key=' + str(client.api_key)
                                awb_date_url_extend = awb_date_url + '&awbno='
                                date_response = requests.get(url=awb_date_url_extend + str(break_here), headers=headers)
                                get_date_time = None
                                if 'data' in json.loads(date_response.content.decode('utf-8')):
                                    shipment_date = json.loads(date_response.content.decode('utf-8'))['data']
                                    data_date = shipment_date['history'][0]['date']
                                    ts = int(data_date)
                                    get_date_time = datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')
                                odoo_expedition = self.env['expedition.info'].search(
                                    [('ex_number', '=', shipment['no'])])
                                if not odoo_expedition:
                                    self.env['expedition.info'].create({
                                        'ex_client': client.name,
                                        'ex_number': shipment['no'],
                                        'ex_status': shipment['status'],
                                        'ex_sender_city': shipment['info']['from_city'],
                                        'ex_sender_country': shipment['info']['from_country'],
                                        'ex_sender_phone': shipment['info']['from_city'],
                                        'ex_receiver_city': shipment['info']['to_city'],
                                        'ex_receiver_country': shipment['info']['to_country'],
                                        'ex_to_address': shipment['info']['to_address'],
                                        'ex_cash_on_delivery': shipment['info']['ramburs'],
                                        'ex_price': shipment['info']['price'],
                                        'ex_date': get_date_time if get_date_time else 'No history found',
                                    })
                                    self.env.cr.commit()
                        else:
                            raise osv.except_osv('', 'Something went wrong while importing shipments')
        except Exception as e:
            Warning(_(str(e)))

    def auto_import_ro_cities(self):
        try:
            clients = self.env['couriermanager.connector'].search([('state', '=', 'connected')])
            for client in clients:
                if client.api_key:
                    baseURL = 'http://app.curiermanager.ro/cscourier/API/'
                    cities_url = baseURL + 'list_cities?api_key=' + client.api_key
                    headers = {
                        'Accept': 'application/json',
                        'connection': 'keep-Alive'
                    }
                    response = requests.get(url=cities_url, headers=headers)
                    if response.status_code == 200:
                        routing_cities = json.loads(response.content.decode('utf-8'))

                        for city in routing_cities:
                            odoo_city = self.env['routing.cities'].search([('cm_city_name', '=', city['name'])])
                            if not odoo_city:
                                self.env['routing.cities'].create({
                                    'cm_city_name': city['name'],
                                    'cm_city_province': city['province'],
                                })
                            self.env.cr.commit()
                    else:
                        raise osv.except_osv('', 'While importing routing cities something '
                                                 'went wrong please try again or check API key.')
        except Exception as e:
            Warning(_(str(e)))

    def auto_import_in(self):
        try:
            clients = self.env['couriermanager.connector'].search([('state', '=', 'connected')])
            for client in clients:
                if client.api_key:
                    today = datetime.date.today()
                    yesterday = today - datetime.timedelta(days=1)
                    invoices_start_date = today.strftime('%d-%m-%Y')
                    invoices_end_date = yesterday.strftime('%d-%m-%Y')
                    baseURL = 'http://app.curiermanager.ro/cscourier/API/'
                    invoices_url = baseURL + 'list_invoices?api_key=' + str(client.api_key)
                    invoices_url_extend = invoices_url + '&from_date=' + str(invoices_start_date) + '&to_date=' + str(
                        invoices_end_date) + '&include_open=true'
                    headers = {
                        'Accept': 'application/json',
                        'connection': 'keep-Alive'
                    }
                    response = requests.get(url=invoices_url_extend, headers=headers)
                    if response.status_code == 200:
                        invoices = json.loads(response.content.decode('utf-8'))

                        if len(invoices) > 0:
                            for invoice in invoices:
                                odoo_invoice = self.env['expedition.invoice'].search([('in_id', '=', invoice['id'])])
                                invoice_date = int(invoice['date'])
                                invoice_todate = int(invoice['toDate'])
                                invoice_fromdate = int(invoice['fromDate'])
                                get_invoice_date = datetime.utcfromtimestamp(invoice_date).strftime('%Y-%m-%d')
                                get_invoice_todate = datetime.utcfromtimestamp(invoice_todate).strftime('%Y-%m-%d')
                                get_invoice_fromdate = datetime.utcfromtimestamp(invoice_fromdate).strftime('%Y-%m-%d')
                                if not odoo_invoice:
                                    self.env['expedition.invoice'].create({
                                        "in_date": get_invoice_date,
                                        "in_number": invoice['no'],
                                        "in_city": invoice['city'],
                                        "in_county": invoice['county'],
                                        "in_emiter": invoice['emiter'],
                                        "in_zone": invoice['zone'],
                                        "in_currency": invoice['currency'],
                                        "in_id": invoice['id'],
                                        "in_value": invoice['value'],
                                        "in_tva": invoice['tva'],
                                        "in_due_days": invoice['days_due'],
                                        "in_to_date": get_invoice_todate,
                                        "in_from_date": get_invoice_fromdate,
                                        "in_name": invoice['name']
                                    })
                                self.env.cr.commit()
                    else:
                        raise osv.except_osv('', 'While importing invoices something went wrong '
                                                 'please try again or check API key.')

        except Exception as e:
            Warning(_(str(e)))

    def prepare_vendor_bill(self):
        invoice_line = self.env['account.move.line']
        list = []
        stock_orders = self.env['expedition.info'].search([])
        for i in stock_orders:
            list.append((i.ex_client))
        res = []
        for i in list:
            if i not in res:
                res.append(i)
        for j in res:
            total = 0

            clients = self.env['expedition.info'].search([("ex_client", '=', j)])

            for l in clients:
                total = total + int(l.ex_price)
            account_obj = self.env['account.account']
            journal = self.env['account.move'].with_context(default_type='sale')._get_default_journal()
            customer = self.env['res.partner'].search([("name", '=', j)])
            product = self.env['product.product'].search([("name", '=', "Delivery Charges")])
            date = fields.Date.today()
            if product:
                print("Product Exist", product.name)
            else:
                product = self.env['product.product'].create({
                    'name': "Delivery Charges", 'type': 'service'
                })
            if customer:
                product = self.env['product.product'].search([("name", '=', "Delivery Charges")])
                print("if", product.id)
                data = {
                    'type': 'out_invoice',
                    'partner_id': customer.id,
                    'invoice_date': str(date),
                    'invoice_line_ids': [(0, 0, {'product_id': product.id,
                                                 'name': "Delivery Charges",
                                                 'quantity': 1,
                                                 'price_unit': total,
                                                 'product_uom_id': False,
                                                 # 'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
                                                 # 'account_id': line.product_id.categ_id.property_account_income_categ_id.id or account_obj.search([('name', '=', 'Incomes')], limit=1).id,
                                                 'journal_id': journal.id})],
                }
                # data.update(self.env['account.move'].default_get(['reference_type']))
                invoice = self.env['account.move'].create(data)
                print(invoice)

            else:
                product = self.env['product.product'].search([("name", '=', "Delivery Charges")])
                print("else", product.id)
                new_client = self.env['res.partner'].create({
                    'name': j,
                })

                data = {
                    'type': 'out_invoice',
                    'partner_id': customer.id,
                    'invoice_date': str(date),
                    'invoice_line_ids': [(0, 0, {'product_id': product.id,
                                                 'name': "Delivery Charges",
                                                 'quantity': 1,
                                                 'price_unit': total,
                                                 'product_uom_id': False,
                                                 # 'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
                                                 # 'account_id': line.product_id.categ_id.property_account_income_categ_id.id or account_obj.search([('name', '=', 'Incomes')], limit=1).id,
                                                 'journal_id': journal.id})],
                }
                # data.update(self.env['account.move'].default_get(['reference_type']))
                invoice = self.env['account.move'].create(data)
                print(invoice)
