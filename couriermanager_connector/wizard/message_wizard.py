from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import osv
import json
import requests
import base64
from datetime import date, datetime
import random


class CustomMessageWizard(models.TransientModel):
    _name = 'message.wizard'

    def get_default(self):
        if self.env.context.get("message", False):
            return self.env.context.get("message")
        return False

    text = fields.Text(readonly=True, default=get_default)


class ExpeditionStatusWizard(models.TransientModel):
    _name = 'expedition.singlestatus'

    ex_number = fields.Char('Number', readonly=True)
    ex_status = fields.Char('Status', readonly=True)
    ex_location = fields.Char('City Name', readonly=True)
    ex_code = fields.Char('City Name', readonly=True)

    def change_expedition_status(self):
        try:
            IrConfigParameter = self.env['ir.config_parameter'].sudo()
            client = IrConfigParameter.get_param('couriermanager.current_client')
            current_client = self.env['couriermanager.client'].search([('id', '=', int(client))])

            baseURL = 'http://app.curiermanager.ro/cscourier/API/'
            expedition_price_url = baseURL + 'change_status?api_key=' + str(current_client.api_key)
            headers = {
                'Accept': 'application/json',
                'connection': 'keep-Alive'
            }
            response = requests.post(url=expedition_price_url + "&awbno=" + str(self.expedition_no)
                                         + "&status=" + self.ex_status, headers=headers)
            if response.status_code == 200:
                expedition_status = json.loads(response.content.decode('utf-8'))['data']
                odoo_expedition = self.env['expedition.info'].search([('ex_number', '=', self.ex_number)])
                odoo_expedition.write({
                    'ex_status': self.ex_status,
                })
                self.env.cr.commit()
            else:
                raise osv.except_osv('', 'While updating expedition\'s status something went wrong please '
                                         'try again or check API key.')
        except Exception as e:
            Warning(_(str(e)))


class OpenExpeditionStatusWizard(models.TransientModel):
    _name = 'expedition_status.wizard'

    expedition_no = fields.Integer('Expedition Number')

    def get_status(self):
        try:
            IrConfigParameter = self.env['ir.config_parameter'].sudo()
            client = IrConfigParameter.get_param('couriermanager.current_client')
            current_client = self.env['couriermanager.client'].search([('id', '=', int(client))])

            baseURL = 'http://app.curiermanager.ro/cscourier/API/'
            expedition_status_url = baseURL + 'get_status?api_key=' + str(current_client.api_key)
            headers = {
                'Accept': 'application/json',
                'connection': 'keep-Alive'
            }
            response = requests.get(url=expedition_status_url + "&awbno=" + str(self.expedition_no), headers=headers)
            if response.status_code == 200:
                expedition_status = json.loads(response.content.decode('utf-8'))['data']
                return self.action_of_button(expedition_status)
            else:
                raise osv.except_osv('', 'While getting expedition\'s status something went wrong please '
                                         'try again or check API key.')

        except Exception as e:
            Warning(_(str(e)))

    def action_of_button(self, expedition_status):
        message_id = self.env['expedition.singlestatus'].create({
            'ex_number': expedition_status['no'],
            'ex_code': expedition_status['code'],
            'ex_location': expedition_status['location'],
            'ex_status': expedition_status['status'],
        })
        return {
            'name': 'Info',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'expedition.singlestatus',
            'res_id': message_id.id,
            'target': 'new',
        }


class OpenExpeditionCancelWizard(models.TransientModel):
    _name = 'expedition_cancel.wizard'

    expedition_no = fields.Integer('Expedition Number')

    def cancel_expedition(self):
        try:
            IrConfigParameter = self.env['ir.config_parameter'].sudo()
            client = IrConfigParameter.get_param('couriermanager.current_client')
            current_client = self.env['couriermanager.client'].search([('id', '=', int(client))])

            baseURL = 'http://app.curiermanager.ro/cscourier/API/'
            expedition_status_url = baseURL + 'cancel?api_key=' + str(current_client.api_key)
            headers = {
                'Accept': 'application/json',
                'connection': 'keep-Alive'
            }
            response = requests.get(url=expedition_status_url + "&awbno=" + str(self.expedition_no), headers=headers)
            if response.status_code == 200:
                expedition_cancel = json.loads(response.content.decode('utf-8'))['data']
            else:
                raise osv.except_osv('', 'While canceling expedition something went wrong please '
                                         'try again or check API key.')

        except Exception as e:
            Warning(_(str(e)))
