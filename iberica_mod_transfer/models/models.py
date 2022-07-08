# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Picking(models.Model):
    _inherit = 'stock.move.line'
    _description = 'test_module.test_module'
    tara = fields.Float(default=1.0, store=True, digits=(12,3))

    peso_bruto = fields.Float(default=1.0, store=True, digits=(12,3))
    peso_neto = fields.Float(default=1.0, store=True, digits=(12,3))
    semielaborado = fields.Boolean()

    peso_neto_x = fields.Float(default=1.0, store=True, digits=(12,3))
    peso_bruto_x = fields.Float(default=1.0, store=True, digits=(12,3))

    @api.onchange('tara', 'peso_bruto', 'qty_done')
    def _traer_datos(self):
        for line in self:
            if self.product_id:
                self.tara = line.picking_id.tara
                self.peso_bruto_x = line.picking_id.product_id.peso_caja_presentacion
                if self.product_id.semielaborado != True :
                    self.semielaborado = False
                    self.peso_neto_x = self.peso_bruto_x * self.qty_done
                    self.peso_neto = self.peso_bruto - self.tara - self.peso_neto_x
                else:
                    self.semielaborado = True
                    self.qty_done = self.peso_bruto - self.tara

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    tara = fields.Float(default=1.0, store=True, digits=(12,3))
    #producto_terminado = fields.Many2one('product.product')
    #product_id = fields.Many2one('product.product', 'Product', related='move_lines.product_id', readonly=True)
