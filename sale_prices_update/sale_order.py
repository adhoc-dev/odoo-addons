# -*- encoding: utf-8 -*-

from openerp.osv import osv
from openerp.osv import fields

class sale_order(osv.osv):
    _inherit = 'sale.order'
       
    def update_prices(self, cr, uid, ids, context=None):
        order_line_obj = self.pool.get('sale.order.line')
        for sale in self.browse(cr, uid, ids):
            items = []
            for line in sale.order_line:
                price = self.pool.get('product.pricelist').price_get(cr, uid, [sale.pricelist_id.id],
                    line.product_id.id, line.product_uom_qty or 1.0, sale.partner_id.id, {
                        'uom': line.product_uom.id,
                        'date': sale.date_order,
                        })[sale.pricelist_id.id]
                order_line_obj.write(cr, uid, [line.id], {'price_unit': price})
        return True
    
sale_order()