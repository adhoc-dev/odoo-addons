# -*- coding    : utf-8 -*-
from openerp import fields, models, api


class sale_order_line_stock(models.Model):
    _inherit = "sale.order.line"

    @api.one
    @api.depends(
        'product_uom_qty',
        'product_id')
    def _fnct_line_stock(self):
        available = False
        if self.order_id.state == 'draft':
            available = self.with_context(
                warehouse=self.order_id.warehouse_id.id
                ).product_id.virtual_available - self.product_uom_qty
        self.virtual_available = available
        if available >= 0.0:
            available = True
        else:
            available = False
        self.virtual_available_boolean = available

    virtual_available = fields.Float(
        compute="_fnct_line_stock", string='Saldo Stock')
    virtual_available_boolean = fields.Boolean(
        compute="_fnct_line_stock", string='Saldo Stock')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
