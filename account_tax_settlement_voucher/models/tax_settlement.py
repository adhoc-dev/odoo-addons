# -*- coding: utf-8 -*-
from openerp import fields, api, models, _
from openerp.exceptions import Warning
import openerp.addons.decimal_precision as dp
import time


class account_tax_settlement(models.Model):
    _inherit = 'account.tax.settlement'

    @api.multi
    def settlement_pay(self):
        self.ensure_one()
        view_id = self.env['ir.model.data'].xmlid_to_res_id(
            'account_voucher.view_vendor_receipt_dialog_form')
        return {
            'name': _("Pay Settlement"),
            'view_mode': 'form',
            'view_id': view_id,
            'view_type': 'form',
            'res_model': 'account.voucher',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
            'context': {
                # 'payment_expected_currency': self.currency_id.id,
                'default_partner_id': self.partner_id.id,
                # 'default_amount': self.residual,
                'default_reference': self.name,
                'close_after_process': True,
                # 'invoice_type': self.type,
                # 'invoice_id': self.id,
                'default_type': 'payment',
                'type': 'payment'
            }
        }
