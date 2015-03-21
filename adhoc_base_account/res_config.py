# -*- coding: utf-8 -*-
from openerp import models, fields


class adhoc_base_configuration(models.TransientModel):
    _inherit = 'adhoc.base.config.settings'

    # Fixes
    module_account_voucher_multic_fix = fields.Boolean(
        'FiX voucher in multi-company father/son environment',
        help="""Installs the account_voucher_multic_fix module.""")
    module_account_multic_fix = fields.Boolean(
        'FiX account in multi-company father/son environment',
        help="""Installs the account_multic_fix module.""")
    module_account_voucher_account_fix = fields.Boolean(
        'FIX vouchers credit/debit account choose. If payment, use credit account; if receipt, use debit account',
        help="""Installs the account_voucher_account_fix module.""")
    module_account_onchange_fix = fields.Boolean(
        'FIX account on changes in multicompany environment',
        help="""Installs the account_onchange_fix module.""")

    # Account modules

    module_account_voucher_contact = fields.Boolean(
        'Show Invoice Partner on voucher lines, usefull when you want to know the contact making a payment',
        help="""Installs the account_voucher_contact module.""")
    module_account_analytic_analysis_mods = fields.Boolean(
        'Make some improovements on contracts managements.',
        help="""Installs the account_analytic_analysis_mods module. Basically:\
            * On creating invoice fill "reference" with contract name\
            * On creating invoice compute tax for total
            * On creating invoice take only tax of contract company
            """)
    module_account_security_modifications = fields.Boolean(
        'Make modifications in security related to accounting (for eg. Inv and Pay. group can choose journals)',
        help="""Installs the account_security_modifications module.""")
    module_account_invoice_merge = fields.Boolean(
        'Allow invoice merge',
        help="""Installs the account_invoice_merge module.""")
    module_currency_rate_update = fields.Boolean(
        'Update currencies rates automatically',
        help="""Installs the currency_rate_update module.""")
    module_account_followup = fields.Boolean(
        'Use account folloup to automate letters for unpaid invoices, with multi-level recalls',
        help="""Installs the account_followup module.""")
    module_account_invoice_tax_wizard = fields.Boolean(
        'Add a wizard to add manual taxes on invoices',
        help="""Installs the account_invoice_tax_wizard module.""")
    module_invoice_fiscal_position_update = fields.Boolean(
        'Invoice Update on Fiscal Position Change',
        help="""Installs the invoice_fiscal_position_update module.""")
    module_account_cancel = fields.Boolean(
        'Allows canceling accounting entries',
        help="""Installs the account_cancel module.""")
    module_account_check = fields.Boolean(
        'Checks Management, issued and third checks',
        help="""Installs the account_check module.""")
    module_account_interests = fields.Boolean(
        'Interests management.',
        help="""Installs the account_interests module.""")
    module_account_invoice_commercial = fields.Boolean(
        'Use commercial on invoices related to partner',
        help="""Installs the account_invoice_commercial module, will also install stock module as it change invoice creation from stock.""")
    module_account_partner_balance = fields.Boolean(
        'See Partner Balance on Partner tree view and balance on account move lines',
        help="""Installs the account_partner_balance module.""")
    module_account_voucher_receipt = fields.Boolean(
        'Manage Payment Receipts',
        help="""Installs the account_voucher_receipt module.""")
    module_account_journal_security = fields.Boolean(
        'Restrict users to some journals',
        help="""Installs the account_journal_security module.""")
    module_account_invoice_adjust = fields.Boolean(
        'Adjust Customer and Suppliers Invoices',
        help="""Installs the account_invoice_adjust module. Allows reconciling between receivable and payable accounts of same partner""")
    module_account_create_journal = fields.Boolean(
        'Configure Payment Journals With a Wizard',
        help="""Installs the account_create_journal module installs checks, payment direction an other modules.""")
    module_account_journal_sequence = fields.Boolean(
        'Add sequence on account journals',
        help="""Installs the account_journal_sequence module.""")
    module_account_payment_direction = fields.Boolean(
        'Allow to set up In or Out on payment journals',
        help="""Installs the account_payment_direction module.""")
    module_account_financial_report_webkit_xls = fields.Boolean(
        'Add XLS export to accounting reports',
        help="""Installs the account_financial_report_webkit_xls module.""")
    module_account_financial_report_webkit = fields.Boolean(
        'Add or replaces the following standard OpenERP financial reports',
        help="""Installs the account_financial_report_webkit module.""")
    module_account_tax_analysis = fields.Boolean(
        'Tax analysis View',
        help="""Installs the account_tax_analysis module. Generate a menu under Accounting / Tax / Tax analysis you are able to group accounting entries by Taxes (VAT codes) and/or financial accounts.""")
    module_account_clean_cancelled_invoice_number = fields.Boolean(
        'Allow canceled invoice number renumber and deletion',
        help="""Installs the account_clean_cancelled_invoice_number module. It adds a button on canceled invoice number so you can choose to remove internal number and then delete it or renumber by re-approving it.""")
    module_multi_store = fields.Boolean(
        'Manage a multi store environment with journals restrictions',
        help="""Installs the multi_store module. The main purpose of this module is to restrict journals access for users on different stores.""")
    module_account_journal_active = fields.Boolean(
        'Allow journals activation/deactivation (adds field "active")',
        help="""Installs the account_journal_active module.""")
    module_account_invoice_company_search = fields.Boolean(
        'Add to Invoice a filter by company and group by Company',
        help="""Installs the account_invoice_company_search module.""")
    module_account_partner_account_summary = fields.Boolean(
        'Add Aeroo Partner Account Summary Report',
        help="""Installs the account_partner_account_summary module.""")
    module_account_bank_voucher = fields.Boolean(
        'Add import vouchers on Bank and Cash Statements',
        help="""Installs the account_bank_voucher module.""")
    module_account_invoice_prices_update = fields.Boolean(
        'Allow prices update on invoices based on pricelist',
        help="""Installs the account_invoice_prices_update module.""")
    module_account_refund_invoice_fix = fields.Boolean(
        'FIX related to invoice refund generation',
        help="""Installs the account_refund_invoice_fix module.""")
    module_account_invoice_journal_filter = fields.Boolean(
        'Add to Invoice a filter by Journal and group by Journal',
        help="""Installs the account_invoice_journal_filter module.""")
    module_account_invoice_pricelist_discount = fields.Boolean(
        'Show on invoice lines discounted price.',
        help="""Installs the account_invoice_pricelist_discount.""")
    module_account_export_csv = fields.Boolean(
        ' Add a wizard that allow you to export a csv file based on accounting journal entries.',
        help="""Installs the account_export_csv.""")

    # Multi Company
    module_web_easy_switch_company = fields.Boolean(
        'Multi company - Enable Company Easy Change',
        help="""Installs the web_easy_switch_company module.""")
    module_inter_company_rules = fields.Boolean(
        'Manager inter company rules',
        help="""Installs the inter_company_rules module.""")
    module_inter_company_move = fields.Boolean(
        'Manager inter company document move',
        help="""Installs the inter_company_move module.""")
