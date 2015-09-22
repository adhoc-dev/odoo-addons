# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api, _
from openerp.exceptions import Warning


class account_invoice(models.Model):
    _inherit = "account.invoice"

    require_purchase_order_number = fields.Boolean(
        string='Sale Require Origin',
        related='partner_id.require_purchase_order_number')
    purchase_order_number = fields.Char(
        'Purchase Order Number',
        readonly=True, states={'draft': [('readonly', False)]})

    @api.multi
    def invoice_validate(self):
        for o in self:
            if o.require_purchase_order_number and o.type in ['out_invoice', 'out_refund']:
                if not o.purchase_order_number:
                    raise Warning(_(
                        'You cannot confirm invoice without a Purchase Order Number for this partner'))
        return super(account_invoice, self).invoice_validate()
