# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Picking(models.Model):
    _inherit = 'stock.quant.package'
    _description = 'test_module.test_module'


    peso_bruto = fields.Float(store=True)

    @api.onchange('shipping_weight')
    def _traer_datos(self):
        if self.name:
            self.shipping_weight = self.env['stock.move.line'].browse(vals.get('peso_bruto'))
            self.peso_bruto = self.shipping_weight
