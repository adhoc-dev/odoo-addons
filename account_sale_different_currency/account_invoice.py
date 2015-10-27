# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import fields, models, api
import openerp.addons.decimal_precision as dp


class account_invoice(models.Model):

    _inherit = 'account.invoice'

    invoice_currency_rate = fields.Float(
        'Invoice Currency Rate',
        digits=(12, 6),
        )
    sale_currency_amount_total = fields.Float(
        compute='_get_sale_currency_amount_total',
        # string='SO Currency Total',
        # waiting for a PR 9081 to fix computed fields translations
        string='Total moneda OV',
        digits=dp.get_precision('Account'),
        )
    sale_currency_id = fields.Many2one(
        'res.currency',
        'Sale Currency',
    )

    @api.one
    @api.depends('invoice_currency_rate', 'amount_total')
    def _get_sale_currency_amount_total(self):
        if self.invoice_currency_rate:
            self.sale_currency_amount_total = (
                self.amount_total / self.invoice_currency_rate)


class account_invoice_line(models.Model):

    _inherit = 'account.invoice.line'

    sale_currency_price_unit = fields.Float(
        'Unit Price in SO Currency',
        digits=dp.get_precision('Product Price')
        )
