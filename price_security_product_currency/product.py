# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from osv import osv
from osv import fields

class product_product(osv.osv):
    _name = 'product.product'
    _inherit = 'product.product'
    
    _columns = {
        'currency_id_copy': fields.related('currency_id', type='many2one', relation="res.currency", readonly=True, store=False,
                                 string='Currency',  help="Moneda utilizada para expresar el Precio de Venta."),
        'currency_list_price_copy': fields.related('currency_list_price', type='float', readonly=True, store=False, 
                                    string='Precio de Venta', help="Precio de venta expresado en la moneda seleccionada."),
    }
    
    def onchange_currency_id(self, cr, uid, ids, currency_id):
        return {'value': {'currency_id_copy': currency_id}}
    
    def onchange_currency_list_price(self, cr, uid, ids, currency_list_price):
        return {'value': {'currency_list_price_copy': currency_list_price}}
    
    def fields_get(self, cr, uid, allfields=None, context=None):
        if not context:
            context = {}
        
        group_obj = self.pool.get('res.groups')
        if group_obj.user_in_group(cr, uid, uid, 'price_security.can_modify_prices', context=context):
            context['can_modify_prices'] = True
        else:
            context['can_modify_prices'] = False
        
        ret = super(product_product, self).fields_get(cr, uid, allfields=allfields, context=context)
        
        if group_obj.user_in_group(cr, uid, uid, 'price_security.can_modify_prices', context=context):
            if 'currency_id_copy' in ret:
                ret['currency_id_copy']['invisible'] = True
            if 'currency_list_price_copy' in ret:
                ret['currency_list_price_copy']['invisible'] = True
        else:
            if 'currency_id' in ret:
                ret['currency_id']['invisible'] = True
            if 'currency_list_price' in ret:
                ret['currency_list_price']['invisible'] = True
        return ret
        
product_product()

