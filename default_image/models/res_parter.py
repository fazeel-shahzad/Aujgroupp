from odoo import models, fields, api, modules
import datetime
from odoo import api, fields, models, tools
from odoo.modules import get_module_resource
import base64
from odoo.modules.module import get_module_resource

class your_class(models.Model):
    _inherit = 'product.template'



    def _get_default_image(self):
        with open(modules.get_module_resource('default_image', 'static/image','icon.png'),'rb') as f:
            return base64.b64encode(f.read())

    image_1920 = fields.Binary(string='Image', default=_get_default_image)

