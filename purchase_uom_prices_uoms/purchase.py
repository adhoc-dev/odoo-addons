# -*- coding: utf-8 -*-
from openerp import models


class purchase_order_line(models.Model):

    """"""

    _inherit = 'purchase.order.line'

    def onchange_product_id(self, cr, uid, ids, pricelist_id, product_id, qty, uom_id,
            partner_id, date_order=False, fiscal_position_id=False, date_planned=False,
            name=False, price_unit=False, state='draft', context=None):
        res = super(purchase_order_line, self).onchange_product_id(
            cr, uid, ids, pricelist_id, product_id, qty=qty, uom_id=uom_id,
            name=name, partner_id=partner_id,
            date_order=date_order, price_unit=price_unit,
            fiscal_position_id=fiscal_position_id,
            date_planned=date_planned, state=state, context=context)

        if product_id:
            context_partner = {'partner_id': partner_id}
            product_obj = self.pool.get('product.product')
            product = product_obj.browse(
                cr, uid, product_id, context=context_partner)
            if 'domain' not in res:
                res['domain'] = {}
            res['domain']['product_uom'] = [
                ('id', 'in', [x.uom_id.id for x in product.uom_price_ids]
                    + [product.uom_id.id] + [product.uom_po_id.id])]
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
