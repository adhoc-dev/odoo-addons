# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class account_voucher_for_migration(models.Model):
    """
    used for migration of this module to l10n_ar_account_voucher
    """

    _inherit = "account.voucher"

    manual_sufix = fields.Integer(
        'Number',
        readonly=True,
        states={'draft': [('readonly', False)]},
        copy=False,
        # added field to copy data
        related='receipt_id.manual_sufix',
        store=True,
        )
    force_number = fields.Char(
        'Force Number',
        readonly=True,
        states={'draft': [('readonly', False)]},
        copy=False,
        # added field to copy data
        related='receipt_id.force_number',
        store=True,
        )
    receiptbook_id = fields.Many2one(
        'account.voucher.receiptbook',
        'ReceiptBook',
        readonly=True,
        states={'draft': [('readonly', False)]},
        # added field to copy data
        related='receipt_id.receiptbook_id',
        store=True,
        )
