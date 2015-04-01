# -*- coding: utf-8 -*-
from openerp import models, fields


class account_tax_withholding(models.Model):
    _name = "account.tax.withholding"
    _description = "Account Withholding Taxes"

    name = fields.Char(
        'Name',
        required=True,
        )
    code = fields.Char(
        'Code',
        required=True,
        )
    application = fields.Selection(
        [('receipt', 'Receipt'), ('payment', 'Payment'), ('all', 'All')],
        'Application',
        required=True,
        )
    active = fields.Boolean(
        'Active',
        help="If the active field is set to False, it will allow you to hide the tax without removing it.")
    # TODO add this field  and other for automation
    # type = fields.Selection(
    #     [('percent', 'Percentage'), ('fixed', 'Fixed Amount'),
    #      ('none', 'None'), ('code', 'Python Code'), ('balance', 'Balance')],
    #     'Type',
    #     required=True,
    #     help="The computation method for the tax amount."
    #     )
    account_receipt_id = fields.Many2one(
        'account.account',
        'Receipt Account',
        required=True,
        )
    account_payment_id = fields.Many2one(
        'account.account',
        'Payment Account',
        required=True,
        )
    account_analytic_receipt_id = fields.Many2one(
        'account.analytic.account',
        'Receipt Analytic Account',
        )
    account_analytic_payment_id = fields.Many2one(
        'account.analytic.account',
        'Payment Analytic Account',
        )
    company_id = fields.Many2one(
        'res.company',
        'Company',
        required=True,
        default=lambda self: self.env['res.company']._company_default_get(
            'account.tax.withholding')
        )
    #
    # Fields used for the Tax declaration
    #
    # TODO ver si necesitamos los base o no
    # receipt_base_code_id = fields.Many2one(
    #     'account.tax.code',
    #     'Receipt Base Code',
    #     help="Use this code for the tax declaration."
    #     )
    receipt_tax_code_id = fields.Many2one(
        'account.tax.code',
        'Receipt Tax Code',
        required=True,
        help="Use this code for the tax declaration.",
        )
    # payment_base_code_id = fields.Many2one(
    #     'account.tax.code',
    #     'Payment Base Code',
    #     help="Use this code for the tax declaration."
    #     )
    payment_tax_code_id = fields.Many2one(
        'account.tax.code',
        'Payment Tax Code',
        required=True,
        help="Use this code for the tax declaration.",
        )
    # TODO ver si necesitamos estos campos
    # base_sign = fields.Float(
    #     'Base Code Sign',
    #     help="Usually 1 or -1.",
    #     digits_compute=get_precision_tax()
    #     )
    # tax_sign = fields.Float(
    #     'Tax Code Sign',
    #     help="Usually 1 or -1.",
    #     digits_compute=get_precision_tax()
    #     )
