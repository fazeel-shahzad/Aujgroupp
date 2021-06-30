# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProductTemplate(models.Model):
	_inherit = 'product.template'

	# @api.model
	# def _get_square_uom_name_from_ir_config_parameter(self):
	# 	""" Get the unit of measure to interpret the `volume` field. By default, we consider
    #     that volumes are expressed in cubic meters. Users can configure to express them in cubic feet
    #     by adding an ir.config_parameter record with "product.volume_in_cubic_feet" as key
    #     and "1" as value.
    #     """
	# 	get_param = self.env['ir.config_parameter'].sudo().get_param
	# 	return "m³" if get_param('product.volume_in_cubic_feet') == '1' else "ft³"
	#
	#
	# @api.model
	# def _get_platten_uom_name_from_ir_config_parameter(self):
	# 	""" Get the unit of measure to interpret the `volume` field. By default, we consider
	# 	that volumes are expressed in cubic meters. Users can configure to express them in cubic feet
	# 	by adding an ir.config_parameter record with "product.volume_in_cubic_feet" as key
	# 	and "1" as value.
	# 	"""
	# 	get_param = self.env['ir.config_parameter'].sudo().get_param
	# 	return "m³" if get_param('product.volume_in_cubic_feet') == '1' else "ft³"
	#
	#
	#
	# def _get_default_square_uom(self):
	# 	return self._get_square_uom_name_from_ir_config_parameter()
	#
	# def _get_default_platten_uom(self):
	# 	return self._get_platten_uom_name_from_ir_config_parameter()

	square = fields.Float(
		'Quadratmeter', compute='_compute_square', digits='Stock Weight',
		inverse='_set_square', store=True)

	platten = fields.Float(
		'Paletten', compute='_compute_platten', digits='Stock Weight',
		inverse='_set_platten', store=True)

	def _set_square(self):
		for template in self:
			if len(template.product_variant_ids) == 1:
				template.product_variant_ids.square = template.square

	def _set_platten(self):
		for template in self:
			if len(template.product_variant_ids) == 1:
				template.product_variant_ids.platten = template.platten


	@api.depends('product_variant_ids', 'product_variant_ids.square')
	def _compute_square(self):
		unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
		for template in unique_variants:
			template.square = template.product_variant_ids.square
		for template in (self - unique_variants):
			template.square = 0.0

	@api.depends('product_variant_ids', 'product_variant_ids.platten')
	def _compute_platten(self):
		unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
		for template in unique_variants:
			template.platten = template.product_variant_ids.platten
		for template in (self - unique_variants):
			template.platten = 0.0


	# square_uom_name = fields.Char(string='Square unit of measure label',
	# 		  default=_get_default_square_uom)
	#
	#
	# platten_uom_name = fields.Char(string='Palette unit of measure label',
	# 					  default=_get_default_platten_uom)
	#

	# square_bool = fields.Boolean(compute = '_compute_square_uom_name',default=False)
	# platten_bool = fields.Boolean(compute = '_compute_platten_uom_name',default=False)

	# def _compute_square_uom_name(self):
	# 	for template in self:
	# 		template.square_bool = False
	# 		template.volume_uom_name = self._get_square_uom_name_from_ir_config_parameter()
	# 		template.square_bool = True
	#
	#
	# def _compute_platten_uom_name(self):
	# 	for template in self:
	# 		template.platten_bool = False
	# 		template.platten_uom_name = self._get_platten_uom_name_from_ir_config_parameter()
	# 		template.platten_bool = True

class ProductProduct(models.Model):
	_inherit = "product.product"

	square = fields.Float('Quadratmeter', digits='Volume')
	platten = fields.Float('Paletten', digits='Stock Weight')