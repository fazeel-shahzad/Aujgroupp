from odoo import models, fields, api, modules
import datetime
from odoo import api, fields, models, tools
from odoo.modules import get_module_resource
import base64
from odoo.modules.module import get_module_resource

class ResUsersInh(models.Model):
    _inherit = 'res.users'

    agent_code = fields.Char('Agent Code')

