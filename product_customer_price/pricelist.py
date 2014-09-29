# -*- coding: utf-8 -*-


import time

from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.translate import _

import openerp.addons.decimal_precision as dp

class product_pricelist(osv.osv):

    _inherit = "product.pricelist"

    #def price_get_multi(self, cr, uid, product_ids, context=None):
    def price_get_multi(self, cr, uid, pricelist_ids, products_by_qty_by_partner, context=None):
        """multi products 'price_get'.
           @param pricelist_ids:
           @param products_by_qty:
           @param partner:
           @param context: {
             'date': Date of the pricelist (%Y-%m-%d),}
           @return: a dict of dict with product_id as key and a dict 'price by pricelist' as value
        """
        results = super(product_pricelist, self).price_get_multi(cr, uid, pricelist_ids, products_by_qty_by_partner, context=context)
        print 'results', results


        currency_obj = self.pool.get('res.currency')
        product_obj = self.pool.get('product.product')
        product_category_obj = self.pool.get('product.category')
        product_uom_obj = self.pool.get('product.uom')
        supplierinfo_obj = self.pool.get('product.supplierinfo')
        price_type_obj = self.pool.get('product.price.type')
        product_customer_price_obj = self.pool.get('product.customer_price')

        # product.product:
        product_ids = [i[0] for i in products_by_qty_by_partner]
        products = product_obj.browse(cr, uid, product_ids, context=context)
        products_dict = dict([(item.id, item) for item in products])


        for product_id, qty, partner in products_by_qty_by_partner:
            print 'partner', partner
            for pricelist_id in pricelist_ids:
                domain = [('product_id','=',product_id),'|',('partner_id','child_of', partner),('partner_id.child_ids','in', partner)]
                product_customer_price_ids = product_customer_price_obj.search(cr, uid, domain, context=context)
                if product_customer_price_ids:
                    product_customer_price = product_customer_price_obj.browse(cr, uid, product_customer_price_ids[0], context=context)
                    price = product_customer_price.price
                    if results.get(product_id):
                        results[product_id][pricelist_id] = price
                    else:
                        results[product_id] = {pricelist_id: price}                    
        return results


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

