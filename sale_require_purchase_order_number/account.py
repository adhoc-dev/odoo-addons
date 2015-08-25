# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class account_invoice(models.Model):
    _inherit = "account.invoice"

    require_purchase_order_number = fields.Boolean(
        string='Sale Require Origin',
        related='partner_id.require_purchase_order_number')
    purchase_order_number = fields.Char(
        'Purchase Order Number',
        readonly=True, states={'draft': [('readonly', False)]})
