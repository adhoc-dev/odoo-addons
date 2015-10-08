# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import Warning


class account_invoice(models.Model):
    _inherit = "account.invoice"

    direct_payment_journal_id = fields.Many2one(
        'account.journal',
        'Direct Payment Method',
        readonly=True,
        domain=[
            ('type', 'in', ('cash', 'bank')),
            ('allow_direct_payment', '=', True)],
        states={'draft': [('readonly', False)]},
        help='If you set a payment method here, after invoice validation, a\
            voucher will be creating and invoice will be paid',
        )

    @api.one
    def create_direct_payment_voucher(self):
        if self.direct_payment_journal_id:
            vals = self.prepare_direct_payment_voucher_vals()
            voucher = self.env['account.voucher'].create(vals)
            voucher.proforma_voucher()

    @api.multi
    def prepare_direct_payment_voucher_vals(self):
        self.ensure_one()
        if not self.direct_payment_journal_id:
            raise Warning(_('No Direct Payment Method Defined'))
        journal = self.direct_payment_journal_id
        partner = self.commercial_partner_id
        company = self.company_id
        voucher_type = self.type in ('out_invoice', 'out_refund') and 'receipt' or 'payment'
        amount = self.type in (
            'out_refund', 'in_refund') and -self.residual or self.residual

        # We set some values in the context
        self = self.with_context(
            payment_expected_currency=self.currency_id.id,
            close_after_process=True,
            invoice_id=self.id,
            ttype=voucher_type,
            )

        # call onchange journal
        journal_vals = self.env['account.voucher'].onchange_journal(
                journal.id,
                False,  # line_ids, TODO ver si agregamos
                False,
                partner.id,
                self.date_invoice,
                amount,
                voucher_type,
                company.id,
                )['value']

        # prepare line_dr and line_cr vals
        line_dr_ids = []
        for dr_line in journal_vals['line_dr_ids']:
            line_dr_ids.append((0, 0, dr_line))

        line_cr_ids = []
        for cr_line in journal_vals['line_cr_ids']:
            line_cr_ids.append((0, 0, cr_line))

        vals = {
            # Values de onchange
            'payment_rate_currency_id': journal_vals['payment_rate_currency_id'],
            'paid_amount_in_company_currency': journal_vals['paid_amount_in_company_currency'],
            'line_dr_ids': line_dr_ids,
            'line_cr_ids': line_cr_ids,
            'currency_id': journal_vals['currency_id'],
            'period_id': journal_vals['period_id'],
            'date': self.date_invoice,
            'pre_line': journal_vals['pre_line'],
            'payment_rate': journal_vals['payment_rate'],
            'account_id': journal_vals['account_id'],

            # other values
            'payment_expected_currency': self.currency_id.id,
            'partner_id': partner.id,
            'amount': amount,
            'reference': self.name,
            'journal_id': journal.id,
            'close_after_process': True,
            'invoice_type': self.type,
            'invoice_id': self.id,
            'type': voucher_type,
        }
        return vals

    @api.multi
    def invoice_validate(self):
        res = super(account_invoice, self).invoice_validate()
        self.create_direct_payment_voucher()
        # for invoice in self:
            # if not invoice.residual or invoice.residual == 0.0:
                # invoice.reconciled = True
        return res
