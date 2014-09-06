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
from tools.translate import _
import decimal_precision as dp
from lxml import objectify
from lxml import etree

class sale_order(osv.osv):
    _name = 'sale.order'
    _inherit = 'sale.order'

    def _get_user_can_modify(self, cr, uid, ids, field_name, args,context=None):
        res = {}
        group_obj = self.pool.get('res.groups')     

        if group_obj.user_in_group(cr, uid, uid, 'price_security.can_modify_prices', context=context):
            flag = True
        else:
            flag = False

        for i in ids:      
            res[i] = flag        
        return res

    user_restrict_prices = fields.function(_get_user_can_modify, type='boolean', string='User Can modify prices'),        
    
    def onchange_pricelist_id(self, cr, uid, ids, pricelist_id, order_lines, context=None):
        ret = super(sale_order, self).onchange_pricelist_id(cr, uid, ids, pricelist_id, order_lines, context=context)
        if 'value' in ret:
            ret['value']['pricelist_id_copy'] = pricelist_id
        return ret
    
    def fields_get(self, cr, uid, allfields=None, context=None):
        ret = super(sale_order, self).fields_get(cr, uid, allfields=allfields, context=context)
        
        group_obj = self.pool.get('res.groups')
        if group_obj.user_in_group(cr, uid, uid, 'price_security.can_modify_prices', context=context):
            if 'pricelist_id_copy' in ret:
                ret['pricelist_id_copy']['invisible'] = True
        else:
            if 'pricelist_id' in ret:
                ret['pricelist_id']['invisible'] = True
        return ret
    
sale_order()


class sale_order_line(osv.osv):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'
    
    def _get_user_can_modify(self, cr, uid, ids, field_name, args,context=None):
        res = {}
        group_obj = self.pool.get('res.groups')     

        if group_obj.user_in_group(cr, uid, uid, 'price_security.can_modify_prices', context=context):
            flag = True
        else:
            flag = False

        for i in ids:      
            res[i] = flag        
        return res
        
    _columns = {
        'price_unit_copy': fields.related('price_unit', type="float", readonly=True, store=False, string='Unit Price'),
        'user_can_modify_prices': fields.function(_get_user_can_modify, type='boolean', string='User Can modify prices'),
        'product_can_modify_prices': fields.related('product_id', 'can_modify_prices', type='boolean', string='Product Can modify prices'),        
        # 'can_modify_prices': fields.boolean('Can modify prices'),
    }
    
    def default_can_modify_prices(self, cr, uid, context=None):
        group_obj = self.pool.get('res.groups')
        if group_obj.user_in_group(cr, uid, uid, 'price_security.can_modify_prices', context=context):
            return True
        else:
            return False
        
    _defaults = {
        # 'can_modify_prices': default_can_modify_prices
    }
    
    def onchange_price_unit(self, cr, uid, ids, price_unit):
        return {'value': {'price_unit_copy': price_unit}}
    
    # def fields_get(self, cr, uid, allfields=None, context=None):
    #     if context == None:
    #         context = {}
    #     group_obj = self.pool.get('res.groups')
    #     if group_obj.user_in_group(cr, uid, uid, 'price_security.can_modify_prices', context=context):
    #         context['can_modify_prices'] = True
    #     else:
    #         context['can_modify_prices'] = False
        
    #     return super(sale_order_line, self).fields_get(cr, uid, allfields=allfields, context=context)
        
    
    
    def create(self, cr, uid, vals, context=None):
        self.check_discount_constrains(cr, uid, False, vals, context=context)
        return super(sale_order_line, self).create(cr, uid, vals, context=context)
    
    def write(self, cr, uid, ids, vals, context=None):
        if not isinstance(ids, list):
            ids = [ids]
        for line_id in ids:
            self.check_discount_constrains(cr, uid, line_id, vals, context=context)
        
        return super(sale_order_line, self).write(cr, uid, ids, vals, context=context)
    
    def check_discount_constrains(self, cr, uid, line_id, vals, context=None):
        discount = vals.get('discount', False)
        pricelist = self.get_order_pricelist(cr, uid, line_id, vals, context=context)
        
        if discount:
            restriction_obj = self.pool.get('price_security.discount_restriction')
            restriction_obj.check_discount_with_restriction(cr, uid, discount, pricelist.id, context=context)
        
    def get_order_pricelist(self, cr, uid, line_id, vals, context=None):
        pricelist = False
        
        order_id = vals.get('order_id', False)
        if order_id:
            order_obj = self.pool.get('sale.order')
            order = order_obj.browse(cr, uid, order_id, context=context)
            if isinstance(order, list):
                order = order[0]
            pricelist = order.pricelist_id
        elif line_id:
            line_obj = self.pool.get('sale.order.line')
            line = line_obj.browse(cr, uid, line_id, context=context)
            if isinstance(line, list):
                line = line[0]
            pricelist = line.order_id.pricelist_id
        
        return pricelist
    
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
        ret = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty=qty, uom=uom, qty_uos=qty_uos,
                            uos=uos, name=name, partner_id=partner_id, lang=lang, update_tax=update_tax, date_order=date_order,
                            packaging=packaging, fiscal_position=fiscal_position, flag=flag, context=context)
        
        if not product:
            return ret
        
        product_obj = self.pool.get('product.product')
        product = product_obj.browse(cr, uid, product, context=context)
        if isinstance(product, list):
            product = product[0]

        group_obj = self.pool.get('res.groups')
        if group_obj.user_in_group(cr, uid, uid, 'price_security.can_modify_prices', context=context):
            ret['value']['user_can_modify_prices'] = True
        else:
            ret['value']['user_can_modify_prices'] = False

        if product.can_modify_prices:
            ret['value']['product_can_modify_prices'] = True
        else:
            ret['value']['product_can_modify_prices'] = False
         
        return ret        

sale_order_line()







