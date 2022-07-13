# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PickingQuant(models.Model):
    _inherit = 'stock.quant.package'
    _description = 'test_module.test_module'


    peso_bruto = fields.Float(store=True, digits=(12,3))

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'test_module.test_module'

    peso_caja_presentacion = fields.Float(store=True, digits=(12,3))
    semielaborado = fields.Boolean()

