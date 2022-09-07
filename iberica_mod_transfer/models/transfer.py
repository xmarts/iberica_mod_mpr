# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class StockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'
    #_description = 'test_module.test_module'

    @api.depends('quant_ids')
    def _compute_weight_bruto(self):
        for package in self:
            peso_bruto = 0.0
            if self.env.context.get('picking_id'):
                # TODO: potential bottleneck: N packages = N queries, use groupby ?
                current_picking_move_line_ids = self.env['stock.move.line'].search([
                    ('result_package_id', '=', package.id),
                    ('picking_id', '=', self.env.context['picking_id'])
                ])
                for ml in current_picking_move_line_ids:
                    peso_bruto += ml.peso_bruto
            package.peso_bruto = peso_bruto

    peso_bruto = fields.Float(compute='_compute_weight_bruto', store=True, digits=(12,3))

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'test_module.test_module'

    peso_caja_presentacion = fields.Float(store=True, digits=(12,3))
    semielaborado = fields.Boolean()

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    quantity = fields.Float(
        'Cantidad a mano',
        help='Quantity of products in this quant, in the default unit of measure of the product',
        readonly=True
    )