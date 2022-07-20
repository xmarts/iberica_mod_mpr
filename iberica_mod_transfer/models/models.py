# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

class Picking(models.Model):
    _inherit = 'stock.move.line'
    _description = 'test_module.test_module'
    tara = fields.Float(default=1.0, store=True, digits=(12,3))

    peso_bruto = fields.Float(default=1.0, store=True, digits=(12,3))
    peso_neto = fields.Float(default=1.0, store=True, digits=(12,3))
    semielaborado = fields.Boolean()
    semielaborado_x = fields.Boolean()

    peso_neto_x = fields.Float(default=1.0, store=True, digits=(12,3))
    peso_bruto_x = fields.Float(default=1.0, store=True, digits=(12,3))

    @api.onchange('tara', 'peso_bruto', 'qty_done', 'product_id')
    def _traer_datos(self):
        for line in self:
            if self.product_id:
                self.tara = line.picking_id.tara
                self.peso_bruto_x = line.picking_id.product_id.peso_caja_presentacion
                self.semielaborado_x = line.product_id.semielaborado
                self.semielaborado = self.semielaborado_x
                if self.semielaborado != True :
                    self.peso_neto_x = self.peso_bruto_x * self.qty_done
                    self.peso_neto = self.peso_bruto - self.tara - self.peso_neto_x
                else:
                    self.qty_done = self.peso_bruto - self.tara

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    tara = fields.Float(default=1.0, store=True, digits=(12,3))
    peso_bruto = fields.Float(store=True, digits=(12,3))
    peso_neto = fields.Float(store=True, digits=(12,3))
    #producto_terminado = fields.Many2one('product.product')
    #product_id = fields.Many2one('product.product', 'Product', related='move_lines.product_id', readonly=True)

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
       # picking_move_lines = self.move_line_ids
        #move_line_ids = picking_move_lines.filtered(lambda ml:
         #       float_compare(ml.qty_done, 0.0, precision_rounding=ml.product_uom_id.rounding) > 0
          #      and not ml.result_package_id
           # )
        if self.move_line_ids:
            for line in self:
                peso_bruto = 0
                peso_neto = 0
                for lineup in line.move_line_ids:
                    peso_bruto = lineup.peso_bruto
                    peso_neto = lineup.peso_neto
        res.update({
                    #'quantity': self.product_uom_qty,
                    'quantity': 0,
                    #'peso_bruto': peso_bruto,

                    })
        return res

    #def button_validate(self, move_line_ids):
     #   res = super(StockPicking, self).button_validate()
      #  #for picking in self:
       # res.update({
        #    'shipping_weight': self.peso_neto,
         #   'peso_bruto': self.peso_bruto,
        #})
        #return res

    