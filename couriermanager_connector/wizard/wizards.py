from odoo import models, fields, api, exceptions, _
from datetime import datetime
from odoo.osv import osv
import requests
import json


class CourierManager(models.TransientModel):
    _name ='couriermanager.wizard'

    cm_client_name = fields.Char(string='Client Name')
    cm_client_api = fields.Char(string='Client\'s API')

    def test_connection(self):
        api_key = self.cm_client_api
        """
            Tests the user's Courier Manager account credentials

            :return:
        """
        if api_key:
            baseURL = 'http://app.curiermanager.ro/cscourier/API/'
            headers = {
                'Accept': 'application/json',
                'connection': 'keep-Alive'
            }
            requestURL = baseURL + 'get_price?api_key=' + api_key
            requesting = requests.get(url=requestURL, headers=headers)
            response = json.loads(requesting.content.decode('utf-8'))
            if 'error' in response:
                raise osv.except_osv('', 'Something went wrong while testing. Please check your API key.')
            else:
                return self.action_of_button()
        else:
            raise osv.except_osv('', 'API Key is missing!')

    def save_client(self):
        try:
            if self.cm_client_name and self.cm_client_api:
                zendesk_company = self.env['couriermanager.client'].search([('name', '=', self.cm_client_name)])
                if not zendesk_company:
                    self.env['couriermanager.client'].create({
                        'name': self.cm_client_name,
                        'api_key': self.cm_client_api,
                    })
                    self.env.cr.commit()
                else:
                    raise osv.except_osv('', 'Client already exists')
            else:
                raise osv.except_osv('', 'Please enter all required fields')
        except Exception as e:
            raise Warning(_(str(e)))

    def action_of_button(self):
        # do what ever login like in your case send an invitation
        ...
        ...
        # don't forget to add translation support to your message _()
        message_id = self.env['message.wizard'].create({'text': "Successfully Connected to CourierManager"})
        return {
            'name': 'Successfull',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'message.wizard',
            'res_id': message_id.id,
            'target': 'new',
        }