# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models


class account_config_settings(models.TransientModel):
    _inherit = 'account.config.settings'

    group_account_voucher_payment = fields.Boolean(
        'Manage Account Voucher Payments Without Receipts',
        implied_group='account_voucher_receipt.group_account_voucher_payment')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
