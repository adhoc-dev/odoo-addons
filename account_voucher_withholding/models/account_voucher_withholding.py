# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp


class account_voucher_withholding(models.Model):
    _name = "account.voucher.withholding"
    _description = "Account Withholding Voucher"

    voucher_id = fields.Many2one(
        'account.voucher',
        'Voucher',
        required=True,
        ondelete='cascade',
        )
    name = fields.Char(
        'Number',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        )
    date = fields.Date(
        'Date',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        default=fields.Date.context_today,
        )
    state = fields.Selection([
            ('draft', 'Draft'),
            ('available', 'Available'),
            ('settled', 'Settled'),
            ('cancel', 'Cancel'),
        ],
        'State',
        required=True,
        track_visibility='onchange',
        )
    tax_withholding_id = fields.Many2one(
        'account.tax.withholding',
        string='Withholding',
        readonly=True,
        states={'draft': [('readonly', False)]},
        )
    comment = fields.Text(
        'Additional Information',
        )
    amount = fields.Float(
        'Amount',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        digits=dp.get_precision('Account'),
        )
    settlement_account_move_id = fields.Many2one(
        'account.move',
        'Settlement Account Move',
        readonly=True,
        )
    # Related fields
    company_id = fields.Many2one(
        'res.company',
        related='voucher_id.company_id',
        string='Company', store=True, readonly=True
        )
    type = fields.Selection(
        related='voucher_id.type',
        string='Type',
        readonly=True,
        )

    @api.one
    @api.constrains('tax_withholding_id', 'voucher_id')
    def check_tax_withholding(self):
        if self.voucher_id.company_id != self.tax_withholding_id.company_id:
            raise Warning(
                _('Voucher and Tax Withholding must belong to the same company'))
