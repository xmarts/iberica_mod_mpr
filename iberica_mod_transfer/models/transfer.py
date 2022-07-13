# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Picking(models.Model):
    _inherit = 'stock.quant.package'
    _description = 'test_module.test_module'


    peso_bruto = fields.Float(store=True, digits=(12,3))

    @api.onchange('shipping_weight')
    def _traer_datos(self):
        if self.shipping_weight:
            self.shipping_weight = self.env['stock.move.line'].browse(vals.get('peso_neto'))
            self.peso_bruto = self.env['stock.move.line'].browse(vals.get('peso_bruto'))

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'test_module.test_module'

    peso_caja_presentacion = fields.Float(store=True, digits=(12,3))
    semielaborado = fields.Boolean()
