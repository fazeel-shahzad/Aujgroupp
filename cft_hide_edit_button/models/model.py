# -*- coding: utf-8 -*-
from odoo.models import BaseModel
from lxml import etree

fields_view_get_extra = BaseModel.fields_view_get 

def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    result = fields_view_get_extra(self,view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
    
    if self.env.user.has_group('cft_hide_edit_button.group_hide_edit_button'):
        if self._name != 'res.users':
            if not self.env.ref('cft_hide_edit_button.group_hide_edit_button').hide_edit_objects:
                temp = etree.fromstring(result['arch'])
                temp.set('edit','0')
                result['arch'] = etree.tostring(temp)
            else:
                models = self.env.ref('cft_hide_edit_button.group_hide_edit_button').hide_edit_objects
                if self._name in models.mapped('model'):
                    temp = etree.fromstring(result['arch'])
                    temp.set('edit','0')
                    result['arch'] = etree.tostring(temp)
    return result

BaseModel.fields_view_get = fields_view_get
