# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

class Picking(models.Model):
    _inherit = 'stock.move.line'
    _description = 'test_module.test_module'
    
    peso_tara = fields.Float(default=1.0, store=True, digits=(12,3))
    peso_bruto = fields.Float(default=1.0, store=True, digits=(12,3))
    peso_neto = fields.Float(default=1.0, store=True, digits=(12,3))
    semielaborado = fields.Boolean()
    semielaborado_x = fields.Boolean()
    picking_relacion = fields.Integer(related="picking_id.relacion")
    peso_neto_x = fields.Float(default=1.0, store=True, digits=(12,3))
    peso_bruto_x = fields.Float(default=1.0, store=True, digits=(12,3))
    tara = fields.Float(default=1.0, store=True, digits=(12,3))

    @api.onchange('peso_tara', 'peso_bruto', 'qty_done', 'product_id')
    def _traer_datos(self):
        for line in self:
            if self.product_id:
                self.picking_relacion = line.picking_id.relacion
                self.peso_tara = line.picking_id.peso_tara
                self.peso_bruto_x = line.picking_id.product_id.peso_caja_presentacion
                self.semielaborado_x = line.product_id.semielaborado
                self.semielaborado = self.semielaborado_x
                if self.semielaborado != True :
                    self.peso_neto_x = self.peso_bruto_x * self.qty_done
                    self.peso_neto = self.peso_bruto - self.peso_tara - self.peso_neto_x
                else:
                    self.qty_done = self.peso_bruto - self.peso_tara

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    peso_tara = fields.Float(default=1.0, store=True, digits=(12,3))
    relacion = fields.Integer(related="picking_type_id.id")
    #default = fields.Char(default="WIP-INTERNAL")
    peso_bruto = fields.Float(store=True, digits=(12,3))
    peso_neto = fields.Float(store=True, digits=(12,3))
    tara = fields.Float(default=1.0, store=True, digits=(12,3))
    #producto_terminado = fields.Many2one('product.product')
    #product_id = fields.Many2one('product.product', 'Product', related='move_lines.product_id', readonly=True)

    @api.depends('picking_type_id')
    def _traer_rel(self):
        for r in self:
            if r.picking_type_id:
                r.relacion = r.picking_type_id.barcode
    
class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    barcode = fields.Char("Código de barra")