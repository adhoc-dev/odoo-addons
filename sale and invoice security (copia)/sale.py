# -*- coding: utf-8 -*-
from openerp import models, fields, _
from openerp.exceptions import except_orm, Warning, RedirectWarning


class sale_order(models.Model):
    _inherit = 'sale.order'
    
    # def action_wait(self, cr, uid, ids, context=None):
    #     for order in self.browse(cr, uid, ids, context=context):
    #         if not order.partner_id or order.partner_id.state != 'approved':
    #             if order.fiscal_position and order.fiscal_position.name.lower() == 'consumidor final':
    #                 if order.payment_term and 'contado' in order.payment_term.name.lower():
    #                     if order.amount_total and order.amount_total < 1000:
    #                         continue
    #             raise Warning (_('Partner no aprobado, no se puede aprobar el pedido ya que el partner no está aprobado. Solo puede validar pedidos de partner no aprobados si son "Consumidores finales" en "Contado" y monto menor a $1000.'))
        
    #     return super(sale_order, self).action_wait(cr, uid, ids, context=context)
