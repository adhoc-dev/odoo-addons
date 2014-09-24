# -*- coding: utf-8 -*-
from openerp import models


class sale_order(models.Model):
    _inherit = "sale.order"

    # def _prepare_order_picking(self, cr, uid, order, context=None):
    #     result = super(sale_order, self)._prepare_order_picking(
    #         cr, uid, order, context=context)
    #     if order.shop_id.warehouse_id and order.shop_id.warehouse_id.stock_journal_id:
    #         result.update(
    #             stock_journal_id=order.shop_id.warehouse_id.stock_journal_id.id)
    #     return result
