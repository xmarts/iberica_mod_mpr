# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Picking(models.Model):
    _inherit = 'stock.move'
    _description = 'test_module.test_module'
    tara = fields.Float(default=1.0, store=True)
    peso_bruto = fields.Float(default=1.0, store=True)
    peso_neto = fields.Float(default=1.0, store=True)

    peso_neto_x = fields.Float(default=1.0, store=True)
    peso_bruto_x = fields.Float(default=1.0, store=True)

    @api.onchange('tara', 'peso_bruto', 'quantity_done')
    def _traer_datos(self):
        for line in self:
            if self.product_id:
                self.peso_bruto_x = line.product_id.weight
                if self.product_id.categ_id != 2 :
                    self.peso_neto_x = self.peso_bruto_x * self.quantity_done
                    self.peso_neto = self.peso_bruto - self.tara - self.peso_neto_x
                else:
                    self.quantity_done = felf.peso_bruto - self.tara
