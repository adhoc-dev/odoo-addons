# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api


class product_product(models.Model):
    _inherit = "product.product"

    @api.one
    def _get_qty(self):
        self.qty = 0
        sale_order_id = self._context.get('active_id', False)
        if sale_order_id:
            lines = self.env['sale.order.line'].search([
                ('order_id', '=', sale_order_id),
                ('product_id', '=', self.id)])
            self.qty = sum([self.env['product.uom']._compute_qty_obj(
                line.product_uom,
                line.product_uom_qty,
                self.uom_id) for line in lines])

    @api.one
    def _set_qty(self):
        sale_order_id = self._context.get('active_id', False)
        qty = self.qty
        if sale_order_id:
            lines = self.env['sale.order.line'].search([
                ('order_id', '=', sale_order_id),
                ('product_id', '=', self.id)])
            if lines:
                (lines - lines[0]).unlink()
                line_data = self.env['sale.order.line'].product_id_change(
                    lines[0].order_id.pricelist_id.id,
                    self.id,
                    qty=qty,
                    partner_id=lines[0].order_id.partner_id.id)
                lines[0].write({
                    'product_uom_qty': qty,
                    'product_uom': self.uom_id.id,
                    'price_unit': line_data['value'].get('price_unit')
                })
            else:
                self.env['sale.order'].browse(
                    sale_order_id).add_products(self.id, qty)

    qty = fields.Integer(
        # TODO poner en ingles cuando el bug de odoo este resuelto
        'Cantidad',
        compute='_get_qty',
        inverse='_set_qty')

    # TODO Borrar si no necesitamos
    # @api.multi
    # def get_product_description(self):
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'product.product',
    #         'view_mode': 'form',
    #         'res_id': self.id,
    #         'target': 'current'
    #     }
