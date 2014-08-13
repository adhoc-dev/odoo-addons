# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
import openerp.addons.decimal_precision as dp


class account_invoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def onchange_company_id(self, company_id, part_id, type, invoice_line, currency_id):
        if self.invoice_line:
            raise Warning(
                _('You cannot change the company of a invoice that has lines. You should delete them first.'))
        return super(account_invoice, self).onchange_company_id(company_id, part_id, type, invoice_line, currency_id)


class account_invoice_line(models.Model):
    _inherit = "account.invoice.line"

    @api.multi
    def product_id_change(self, product, uom_id, qty=0, name='', type='out_invoice',
                          partner_id=False, fposition_id=False, price_unit=False, currency_id=False,
                          context=None, company_id=None):
        res = super(account_invoice_line, self).product_id_change(product, uom_id, qty=qty, name=name, type=type,
                                                                  partner_id=partner_id, fposition_id=fposition_id, price_unit=price_unit, currency_id=currency_id,
                                                                  context=context, company_id=company_id)
        if not 'value' in res:
            res['value'] = {}

        fpos = self.env['account.fiscal.position'].browse(fposition_id)
        if 'invoice_line_tax_id' in res['value']:
            tax_ids = res['value']['invoice_line_tax_id']
            taxes = self.env['account.tax'].search(
                [('id', 'in', tax_ids), ('company_id', '=', company_id)])
            taxes = fpos.map_tax(taxes)
            res['value']['invoice_line_tax_id'] = taxes.ids
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
