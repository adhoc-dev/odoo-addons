# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
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
        )
    date = fields.Date(
        'Date',
        required=True,
        default=fields.Date.context_today,
        )
    # state = fields.Selection(
    #     # [
    #     #     ('draft', 'Draft'),
    #     #     ('available', 'Available'),
    #     #     ('settled', 'Settled'),
    #     #     ('cancel', 'Cancel'),
    #     # ],
    #     string='State',
    #     related='voucher_id.state',
    #     default='draft',
    #     required=True,
    #     track_visibility='onchange',
    #     )
    tax_withholding_id = fields.Many2one(
        'account.tax.withholding',
        string='Withholding',
        required=True,
        )
    comment = fields.Text(
        'Additional Information',
        )
    amount = fields.Float(
        'Amount',
        required=True,
        digits=dp.get_precision('Account'),
        )
    move_line_id = fields.Many2one(
        'account.move.line',
        'Journal Item',
        readonly=True,
        )
    # Related fields
    partner_id = fields.Many2one(
        related='voucher_id.partner_id',
        store=True, readonly=True,
        )
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
            raise Warning(_(
                'Voucher and Tax Withholding must belong to the same company'))
