# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api, _


class sale_order(models.Model):
    _inherit = "sale.order"

    @api.multi
    def add_products_to_quotation(self):
        self.ensure_one()
        view_id = self.env['ir.model.data'].xmlid_to_res_id(
            'sale_quotation_products.product_product_tree_view')
        res = {
            'type': 'ir.actions.act_window',
            'res_model': 'product.product',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'views': [(view_id, 'tree'), (False, 'form')],
            # 'view_id': view_id,
            'target': 'current',
            'name': _('Quotation Products'),
        }
        return res

    @api.multi
    def add_products(self, product_ids, qty):
        self.ensure_one()
        for product in self.env['product.product'].browse(product_ids):
            line_data = self.env['sale.order.line'].product_id_change(
                self.pricelist_id.id,
                product.id,
                qty=1,
                partner_id=self.partner_id.id)
            val = {
                'product_uom_qty': qty,
                'order_id': self.id,
                'product_id': product.id or False,
                'product_uom': line_data['value'].get('product_uom'),
                'price_unit': line_data['value'].get('price_unit'),
                'tax_id': [(6, 0, line_data['value'].get('tax_id'))],
            }
            self.env['sale.order.line'].create(val)
