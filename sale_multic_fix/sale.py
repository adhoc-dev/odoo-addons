# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
import openerp.addons.decimal_precision as dp


# class sale_order(models.Model):
#     _inherit = "sale.order"

#     @api.multi
#     def onchange_company_id(self, company_id, part_id, type, invoice_line, currency_id):
#         if self.invoice_line:
#             raise Warning(
#                 _('You cannot change the company of a invoice that has lines. You should delete them first.'))
# return super(account_invoice, self).onchange_company_id(company_id,
# part_id, type, invoice_line, currency_id)

class sale_order_line(models.Model):
    _inherit = "sale.order.line"

    # @api.multi
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
        res = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty=qty, uom=uom, qty_uos=qty_uos,
                                                             uos=uos, name=name, partner_id=partner_id, lang=lang,
                                                             update_tax=update_tax, date_order=date_order, packaging=packaging, 
                                                             fiscal_position=fiscal_position, flag=flag, context=context)
        if not 'value' in res:
            res['value'] = {}
        # tomamos la company del contexto porque no tenemos otra forma de saberla (ni sale order, ni warehouse)
        company_id = context.get('company_id', False)
        if company_id:
            fpos = self.pool['account.fiscal.position'].browse(cr, uid, fiscal_position)
            if 'tax_id' in res['value']:
                tax_ids = res['value']['tax_id']
                taxes_ids = self.pool['account.tax'].search(cr, uid, 
                    [('id', 'in', tax_ids), ('company_id', '=', company_id)], context=context)
                taxes = self.pool['account.tax'].browse(cr, uid, taxes_ids, context=context)
                res['value']['tax_id'] = self.pool['account.fiscal.position'].map_tax(cr, uid, fpos, taxes)
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
