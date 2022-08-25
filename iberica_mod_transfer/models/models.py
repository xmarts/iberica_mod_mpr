# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

class Picking(models.Model):
    _inherit = 'stock.move.line'
    _description = 'test_module.test_module'
    
    peso_tara = fields.Float(string="Tara", default=0.0, store=True, digits=(12,3))
    peso_bruto = fields.Float(default=0.0, store=True, digits=(12,3))
    peso_neto = fields.Float(default=0.0, store=True, digits=(12,3))
    semielaborado = fields.Boolean()
    semielaborado_x = fields.Boolean()
    picking_relacion = fields.Integer(related="picking_id.relacion")
    peso_neto_x = fields.Float(default=1.0, store=True, digits=(12,3))
    peso_bruto_x = fields.Float(default=1.0, store=True, digits=(12,3))
    tara = fields.Float(default=1.0, store=True, digits=(12,3))
    package_id = fields.Many2one(
        'stock.quant.package', 
        string="Paquete origen", 
        ondelete='restrict',
        check_company=True,
        domain="['product_id', 'in', 'package_id.product_id']"
    )

    @api.onchange('peso_tara', 'peso_bruto', 'qty_done', 'product_id')
    def _traer_datos(self):
        for line in self:
            if line.product_id:
                line.picking_relacion = line.picking_id.relacion
                line.peso_tara = line.picking_id.peso_tara
                line.peso_bruto_x = line.picking_id.product_id.peso_caja_presentacion
                line.semielaborado_x = line.product_id.semielaborado
                line.semielaborado = line.semielaborado_x
                if line.semielaborado != True :
                    line.peso_neto_x = line.peso_bruto_x * line.qty_done
                    line.peso_neto = line.peso_bruto - line.peso_tara - line.peso_neto_x
                else:
                    if line.peso_bruto != 0:
                        line.qty_done = line.peso_bruto - line.peso_tara

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    peso_tara = fields.Float(default=1.0, store=True, digits=(12,3))
    relacion = fields.Integer(related="picking_type_id.id")
    peso_bruto = fields.Float(store=True, digits=(12,3))
    peso_neto = fields.Float(store=True, digits=(12,3))
    tara = fields.Float(default=1.0, store=True, digits=(12,3))

    @api.depends('picking_type_id')
    def _traer_rel(self):
        for r in self:
            if r.picking_type_id:
                r.relacion = r.picking_type_id.barcode
    
class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    barcode = fields.Char("Código de barra")