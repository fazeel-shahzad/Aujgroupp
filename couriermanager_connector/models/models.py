# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.osv import osv
from datetime import datetime, timezone
import requests
from dateutil.relativedelta import relativedelta
import pdfkit
import urllib.parse
from hashlib import sha256
from hmac import HMAC
import json

INTERVAL_UNITS = [
        ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('work_days', 'Work Days'),
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months'),
    ]

_intervalTypes = {
    'work_days': lambda interval: relativedelta(days=interval),
    'days': lambda interval: relativedelta(days=interval),
    'hours': lambda interval: relativedelta(hours=interval),
    'weeks': lambda interval: relativedelta(days=7 * interval),
    'months': lambda interval: relativedelta(months=interval),
    'minutes': lambda interval: relativedelta(minutes=interval),
}


class CourierManagerConnector(models.Model):
    _name = "couriermanager.connector"

    name = fields.Char(string='Client Name')
    api_key = fields.Char(string='API Key')
    state = fields.Selection([("draft", 'Draft'), ("connected", 'Connected')], default='connected')

    def button_disconnect(self):
        self.write({'state': 'draft'})
        return True

    def test_connection(self):
        """
            Tests the user's Courier Manager account credentials

            :return:
        """
        if self.api_key:
            baseURL = 'http://app.curiermanager.ro/cscourier/API/'
            headers = {
                'Accept': 'application/json',
                'connection': 'keep-Alive'
            }
            requestURL = baseURL + 'get_price?api_key=' + self.api_key
            requesting = requests.get(url=requestURL, headers=headers)
            response = requesting

            if 'error' in response:
                raise osv.except_osv('', 'Something went wrong while testing. Please check your API key.')
            else:
                self.write({'state': 'connected'})
                return True
        else:
            raise osv.except_osv('', 'API Key is missing!')


class ExpeditionPrice(models.Model):
    _name = "expedition.price"

    cm_client_name = fields.Char('Client Name')
    cm_expedition_price = fields.Float('Expedition Price')
    cm_expedition_zone = fields.Char('Expedition Zone')


class RoutingCities(models.Model):
    _name = "routing.cities"

    cm_city_name = fields.Char('City Name')
    cm_city_province = fields.Char('Province')


class ExpeditionInfo(models.Model):
    _name = "expedition.info"

    ex_client = fields.Char('Client Name')
    ex_number = fields.Char('Number')
    ex_status = fields.Char('Status')
    ex_sender_city = fields.Char('Sender City')
    ex_sender_country = fields.Char('Sender Country')
    ex_sender_phone = fields.Char('Sender Phone')
    ex_receiver_city = fields.Char('Receiver City')
    ex_receiver_country = fields.Char('Receiver Country')
    ex_to_address = fields.Text('To Address')
    ex_cash_on_delivery = fields.Char('Cash On Delivery')
    ex_price = fields.Char('Price')
    ex_date = fields.Char('Date')
    ex_bol = fields.Boolean()


class ExpeditionInvoice(models.Model):
    _name = "expedition.invoice"

    in_id = fields.Char('Id')
    in_date = fields.Char('Date')
    in_number = fields.Char('Number')
    in_city = fields.Char('City')
    in_county = fields.Char('County')
    in_emiter = fields.Char('Emiter')
    in_zone = fields.Char('Zone')
    in_currency = fields.Char('Currency')
    in_value = fields.Char('Value')
    in_tva = fields.Char('Tax Value')
    in_due_days = fields.Char('Due Days')
    in_to_date = fields.Char('To Date')
    in_from_date = fields.Char('From Date')
    in_name = fields.Char('Name')
