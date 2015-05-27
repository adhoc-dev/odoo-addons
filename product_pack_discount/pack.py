# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import fields, models, api


class product_pack(models.Model):
    _inherit = 'product.pack.line'

    discount = fields.Float('Discount')

    @api.multi
    def get_sale_order_line_vals(self, line, order, sequence, fiscal_position):
        vals = super(product_pack, self).get_sale_order_line_vals(
            line, order, sequence, fiscal_position)
        if self.discount:
            vals['discount'] = self.discount
        return vals
