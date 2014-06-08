# -*- coding: utf-8 -*-
##############################################################################
#
#    Ingenieria ADHOC - ADHOC SA
#    https://launchpad.net/~ingenieria-adhoc
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
import time

class product_template(osv.osv):
    _name = 'product.template'
    _inherit = 'product.template' 

    def _get_sale_price_currency(self, cr, uid, ids, name, args, context=None):
        result = {}
        price_type_obj = self.pool.get('product.price.type')
        price_type_ids = price_type_obj.search(cr, uid, [('field','=','list_price')], context=context)
        currency_id = False
        if price_type_ids:
            currency_id = price_type_obj.browse(cr, uid, price_type_ids[0], context=context).currency_id.id
        
        for i in ids:
            result[i] = currency_id
        return result    
    
    _columns = {
        'sale_price_currency_id':fields.function(_get_sale_price_currency, type='many2one', relation='res.currency', string='Currency', readonly=True,),
        'currency_id':fields.many2one('res.currency', 'Currency', required=True, help="Currency used for the Currency List Price."),
        'currency_list_price': fields.float('Currency List Price', digits_compute=dp.get_precision('Sale Price'),
                                            help="List Price on selected currency."),
    }

    def get_currency_id(self, cr, uid, context=None):
        price_type_obj = self.pool.get('product.price.type')
        price_type_ids = price_type_obj.search(cr, uid, [('field','=','list_price')], context=context)
        res = False
        if price_type_ids:
            res = price_type_obj.browse(cr, uid, price_type_ids[0], context=context).currency_id.id
        return res

    _defaults = {
        'currency_id': get_currency_id,
    }

    def write(self, cr, uid, ids, vals, context=None):
        if 'currency_list_price' in vals or 'currency_id' in vals or 'list_price' in vals:
            product_id = ids
            if isinstance(product_id, list):
                product_id = product_id[0]
            product = self.pool.get('product.template').browse(cr, uid, product_id, context=context)
            if 'currency_list_price' in vals:
                currency_list_price = vals['currency_list_price']
            else:
                currency_list_price = product.currency_list_price

            if 'currency_id' in vals:
                currency_id = vals['currency_id']
            else:
                currency_id = product.currency_id.id
            if currency_list_price and currency_id:
                list_price = self.compute_list_price(cr, uid, currency_id, currency_list_price, context=context)
                vals['list_price'] = list_price
        return super(product_template, self).write(cr, uid, ids, vals, context=context)
    
    def create(self, cr, uid, vals, context=None):
        if 'currency_list_price' in vals and 'currency_id' in vals:
            currency_list_price = vals['currency_list_price']
            currency_id = vals['currency_id']
            list_price = self.compute_list_price(cr, uid, currency_id, currency_list_price, context=context)
            vals['list_price'] = list_price
        ret = super(product_template, self).create(cr, uid, vals, context=context)
        return ret
    
    def compute_list_price(self, cr, uid, product_currency_id, currency_list_price, context=None):
        price_type_id = self.pool.get('product.price.type').search(cr, uid, [('field', '=', 'list_price')], context=context)
        if isinstance(price_type_id, list):
            price_type_id = price_type_id[0]
        price_type = self.pool.get('product.price.type').browse(cr, uid, price_type_id, context=context)
        list_price = self.pool.get('res.currency').compute(cr, uid,
                                                           product_currency_id,
                                                           price_type.currency_id.id,
                                                           currency_list_price,
                                                           context=context)
        return list_price
    
    def update_list_prices(self, cr, uid, ids, context=None):
        # We use the admin user id so it can access the product.price.tyoe and res.currency in case the user accessing the
        # price does not have rights to do that.
        for product_template in self.browse(cr, uid, ids, context=None):
            currency_id = product_template.currency_id.id
            currency_list_price = product_template.currency_list_price
            list_price = self.compute_list_price(cr, uid, currency_id, currency_list_price, context=context)        
            vals = {'list_price': list_price}
            self.write(cr, 1, product_template.id, vals, context=context)
        return True
    