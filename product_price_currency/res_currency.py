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

import re
import time

from openerp import tools
from openerp.osv import fields, osv
from openerp.tools import float_round, float_is_zero, float_compare
from openerp.tools.translate import _


class res_currency(osv.osv):
    _inherit = "res.currency"


    def update_prices(self, cr, uid, ids, context=None):
        price_type_obj = self.pool.get('product.price.type')
        product_template_obj = self.pool.get('product.template')
        sale_price_currency_id = False
        
        price_type_ids = price_type_obj.search(cr, uid, [('field','=','list_price')], context=context)
        if price_type_ids:
            sale_price_currency_id = price_type_obj.browse(cr, uid, price_type_ids[0], context=context).currency_id.id
        
        for record in self.browse(cr, uid, ids, context=context):
            if sale_price_currency_id == record.id:
                print 'Sale Price Currency change, updating all products...'
                product_template_ids = product_template_obj.search(cr, uid, [])
            else:
                print 'Currency change, updating affected products...'
                product_template_ids = product_template_obj.search(cr, uid, [('currency_id','=',record.id)])
            product_template_obj.update_list_prices(cr, uid, product_template_ids, context=context)
        return True

class res_currency_rate(osv.osv):
    _inherit = "res.currency.rate"
    
    def write(self, cr, uid, ids, vals, context=None):   
        res = super(res_currency_rate, self).write(cr, uid, ids, vals, context=context)     
        currency_obj = self.pool.get('res.currency')
        currency_ids = []
        if 'rate' in vals or 'name' in vals:
            for record in self.browse(cr, uid, ids, context=context):
                currency_ids.append(record.currency_id.id)
            currency_obj.update_prices(cr, uid, currency_ids, context=context)
        return res

    def create(self, cr, uid, vals, context=None):   
        res = super(res_currency_rate, self).create(cr, uid, vals, context=context)
        currency_ids = [vals.get('currency_id')]
        self.pool.get('res.currency').update_prices(cr, uid, currency_ids, context=context)
        return res

    def unlink(self, cr, uid, ids, context=None):   
        currency_obj = self.pool.get('res.currency')
        currency_ids = []
        for record in self.browse(cr, uid, ids, context=context):
            currency_ids.append(record.currency_id.id)
        res = super(res_currency_rate, self).unlink(cr, uid, ids, context=context)
        currency_obj.update_prices(cr, uid, currency_ids, context=context)
        return res