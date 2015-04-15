# -*- coding: utf-8 -*-
from openerp import models, api


class account_invoice(models.Model):
    _inherit = 'account.invoice'
    """Agregamos algunas funciones relativas a account pero que necesitan de
    sale en este modulo"""

    @api.multi
    def split_invoice(self, lines_to_split):
        '''
        Update sale_orders m2m invoice_ids fields with new invoices
        '''
        res = super(account_invoice, self).split_invoice(lines_to_split)
        for invoice_id, new_invoice in res.iteritems():
            if new_invoice:
                sale_orders = self.env['sale.order'].search(
                    [('invoice_ids', 'in', [invoice_id])])
                sale_orders.write({'invoice_ids': [(4, new_invoice.id)]})
        return res

    def confirm_paid(self, cr, uid, ids, context=None):
        res = super(account_invoice, self).confirm_paid(
            cr, uid, ids, context=context)
        self.check_sale_order_paid(cr, uid, ids, context=context)
        return res

    def check_sale_order_paid(self, cr, uid, ids, context=None):
        '''Esta funcion la hacemos para verificar si toda la orden de venta fue pagada en el caso de
         'pago antes de la entrega' porque el problema es el siguiente, de manera original openerp
         genera una factura que queda vinculada por el subflow avisando cuando fue pagada a la orden de venta, 
         el problema es que en este caso tendriamos mas de una factura ligada, por eso el chequeo hay que hacerlo aparte
         '''
        sale_order_obj = self.pool.get('sale.order')
        so_ids = sale_order_obj.search(
            cr, uid, [('invoice_ids', 'in', ids)], context=context)
        for so in sale_order_obj.browse(cr, uid, so_ids, context=context):
            if so.order_policy == 'prepaid' and so.invoiced:
                so.signal_workflow('subflow.paid')
        return True
