# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning


class account_invoice(models.Model):
    _inherit = 'account.invoice'

    # _columns = {
    #     'payment_term_copy': fields.related('payment_term', type="many2one", relation="account.payment.term",
    #                                         readonly=True, store=False, string=u'Plazo de Pago'),
    #     'fiscal_position_copy': fields.related('fiscal_position', type="many2one", relation="account.fiscal.position",
    #                                            readonly=True, store=False, string=u'Posición Fiscal'),
    # }

    # def onchange_payment_term(self, cr, uid, ids, payment_term):
    #     return {'value': {'payment_term_copy': payment_term}}

    # def onchange_fiscal_position(self, cr, uid, ids, fiscal_position):
    #     return {'value': {'fiscal_position_copy': fiscal_position}}

    # def fields_get(self, cr, user, allfields=None, context=None, write_access=True):
    #     ret = super(account_invoice, self).fields_get(
    #         cr, user, allfields=allfields, context=context)
    #     group_obj = self.pool.get('res.groups')
    #     if group_obj.user_in_group(cr, user, user, 'partner_state.approve_partners', context=context):
    #         if 'payment_term_copy' in ret:
    #             ret['payment_term_copy']['invisible'] = True
    #         if 'fiscal_position_copy' in ret:
    #             ret['fiscal_position_copy']['invisible'] = True
    #     else:
    #         if 'payment_term' in ret:
    #             ret['payment_term']['invisible'] = True
    #         if 'fiscal_position' in ret:
    #             ret['fiscal_position']['invisible'] = True
    #     return ret

    @api.multi
    def action_date_assign(self):
        for invoice in self:
            if not invoice.partner_id or (invoice.partner_id.customer and invoice.partner_id.state != 'approved'):
                if invoice.fiscal_position and invoice.fiscal_position.name.lower() == 'consumidor final':                
                    if invoice.payment_term and 'contado' in invoice.payment_term.name.lower():
                        if invoice.amount_total and invoice.amount_total < 1000:
                            continue
                mensaje = _('Partner no aprobado, no se puede aprobar el pedido ya que el partner no está aprobado. Solo puede validar pedidos de partner no aprobados si son "Consumidores finales" en "Contado" y monto menor a $1000.')
                raise Warning(mensaje)
        return super(account_invoice, self).action_date_assign(self)