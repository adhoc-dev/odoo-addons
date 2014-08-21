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
import inspect

class sale_order(osv.osv):
    _name = 'sale.order'
    _inherit = 'sale.order'
    
    _columns = {
        'payment_term_copy': fields.related('payment_term', type="many2one", relation="account.payment.term",
                                            readonly=True, store=False, string=u'Termino de Pago'),
        'fiscal_position_copy': fields.related('fiscal_position', type="many2one", relation="account.fiscal.position",
                                            readonly=True, store=False, string=u'Posición Fiscal'),
    }
    
    def onchange_payment_term(self, cr, uid, ids, payment_term):
        return {'value': {'payment_term_copy': payment_term}}
    
    def onchange_fiscal_position(self, cr, uid, ids, fiscal_position):
        return {'value': {'fiscal_position_copy': fiscal_position}}
    
    def onchange_partner_id(self, cr, uid, ids, part):
        ret = super(sale_order, self).onchange_partner_id(cr, uid, ids, part)
        print ret
        return ret
    
    def fields_get(self, cr, user, allfields=None, context=None, write_access=True):
        ret = super(sale_order, self).fields_get(cr, user, allfields=allfields, context=context)
        
        group_obj = self.pool.get('res.groups')
        if group_obj.user_in_group(cr, user, user, 'partner_state.approve_partners', context=context):
            if 'payment_term_copy' in ret:
                ret['payment_term_copy']['invisible'] = True
            if 'fiscal_position_copy' in ret:
                ret['fiscal_position_copy']['invisible'] = True
        else:
            if 'payment_term' in ret:
                ret['payment_term']['invisible'] = True
            if 'fiscal_position' in ret:
                ret['fiscal_position']['invisible'] = True
        return ret
    
    def action_wait(self, cr, uid, ids, context=None):
        for order in self.browse(cr, uid, ids, context=context):
            if not order.partner_id or order.partner_id.state != 'approved':
                if order.fiscal_position and order.fiscal_position.name.lower() == 'consumidor final':
                    if order.payment_term and 'contado' in order.payment_term.name.lower():
                        if order.amount_total and order.amount_total < 1000:
                            continue
                titulo = 'Cliente no aprobado'
                mensaje = 'Partner no aprobado, no se puede aprobar el pedido ya que el partner no está aprobado. Solo puede validar pedidos de partner no aprobados si son "Consumidores finales" en "Contado" y monto menor a $1000.'
                raise osv.except_osv(titulo, mensaje)
        
        return super(sale_order, self).action_wait(cr, uid, ids, context=context)
    
sale_order()
