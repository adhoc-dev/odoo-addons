# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api


class purchase_order_line(models.Model):

    """"""

    _inherit = 'purchase.order.line'

    @api.multi
    def onchange_product_id(
            self, pricelist_id, product_id, qty, uom_id, partner_id,
            date_order=False, fiscal_position_id=False, date_planned=False,
            name=False, price_unit=False, state='draft'):
        res = super(purchase_order_line, self).onchange_product_id(
            pricelist_id, product_id, qty=qty, uom_id=uom_id, name=name,
            partner_id=partner_id, date_order=date_order,
            price_unit=price_unit, fiscal_position_id=fiscal_position_id,
            date_planned=date_planned, state=state)

        if product_id:
            product = self.env['product.product'].with_context(partner_id=partner_id).browse(
                product_id)
            if 'domain' not in res:
                res['domain'] = {}
            res['domain']['product_uom'] = [
                ('id', 'in', [x.uom_id.id for x in product.uom_price_ids]
                    + [product.uom_id.id] + [product.uom_po_id.id])]
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
