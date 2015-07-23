# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
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

class purchase_order_line(models.Model):
    _inherit = "purchase.order.line"

    def onchange_product_id(self, cr, uid, ids, pricelist_id, product_id, qty, uom_id,
            partner_id, date_order=False, fiscal_position_id=False, date_planned=False,
            name=False, price_unit=False, state='draft', context=None):
        res = super(purchase_order_line, self).onchange_product_id(cr, uid, ids, pricelist_id, product_id, qty, uom_id,
            partner_id, date_order=date_order, fiscal_position_id=fiscal_position_id, date_planned=date_planned,
            name=name, price_unit=price_unit, state=state, context=context)
        
        if not context:
            context = {}
            
        if not 'value' in res:
            res['value'] = {}
        company_id = context.get('company_id', False)
        if company_id:
            fpos = self.pool['account.fiscal.position'].browse(cr, uid, fiscal_position_id)
            if 'taxes_id' in res['value']:
                tax_ids = res['value']['taxes_id']
                taxes_ids = self.pool['account.tax'].search(cr, uid, 
                    [('id', 'in', tax_ids), ('company_id', '=', company_id)], context=context)
                taxes = self.pool['account.tax'].browse(cr, uid, taxes_ids, context=context)
                res['value']['taxes_id'] = self.pool['account.fiscal.position'].map_tax(cr, uid, fpos, taxes)
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
