# -*- coding: utf-8 -*-
import logging
from openerp.osv import fields, osv

_logger = logging.getLogger(__name__)

class adhoc_base_configuration(osv.osv_memory):
    _name = 'adhoc.base.config.settings'
    _inherit = 'res.config.settings'

    _columns = {
        #Fixes
        'module_account_voucher_multic_fix': fields.boolean('FiX voucher in multi-company father/son environment',
            help="""Installs the account_voucher_multic_fix module."""),
        'module_account_multic_fix': fields.boolean('FiX account in multi-company father/son environment',
            help="""Installs the account_multic_fix module."""),
        'module_sale_multic_fix': fields.boolean('FiX sale in multi-company father/son environment',
            help="""Installs the sale_multic_fix module."""),
        'module_purchase_multic_fix': fields.boolean('FiX purchase in multi-company father/son environment',
            help="""Installs the purchase_multic_fix module."""),
        'module_account_voucher_account_fix': fields.boolean('FiX vouchers so that if payment use journal credit account, if receipt use journal debit account',
            help="""Installs the account_voucher_account_fix module."""),
        'module_account_onchange_fix': fields.boolean('Fix on change partner or company in multicompany environment',
            help="""Installs the account_onchange_fix module."""),        
        
        # Account modules
        'module_account_cancel': fields.boolean('Allows canceling accounting entries',
            help="""Installs the account_cancel module."""),
        'module_account_check': fields.boolean('Checks Management, issued and third checks',
            help="""Installs the account_check module."""),
        'module_account_interests': fields.boolean('Interests management.',
            help="""Installs the account_interests module."""),
        'module_account_invoice_commercial': fields.boolean('Use commercial on invoices related to partner',
            help="""Installs the account_invoice_commercial module, will also install stock module as it change invoice creation from stock."""),
        'module_account_partner_balance': fields.boolean('Aeroo Partner Balance Report',
            help="""Installs the account_partner_balance module."""),
        'module_account_voucher_receipt': fields.boolean('Manage Payment Receipts',
            help="""Installs the account_voucher_receipt module."""),
        'module_account_journal_security': fields.boolean('Restrict users to some journals',
            help="""Installs the account_journal_security module."""),
        'module_account_invoice_adjust': fields.boolean('Adjust Customer and Suppliers Invoices',
            help="""Installs the account_invoice_adjust module. Allows reconciling between receivable and payable accounts of same partner"""),        
        'module_account_create_journal': fields.boolean('Configure Payment Journals With a Wizard',
            help="""Installs the account_create_journal module installs checks, payment direction an other modules."""),
        'module_account_journal_sequence': fields.boolean('Add sequence on account journals',
            help="""Installs the account_journal_sequence module."""),
        'module_account_payment_direction': fields.boolean('Allow to set up In or Out on payment journals',
            help="""Installs the account_payment_direction module."""),
        'module_account_financial_report_webkit_xls': fields.boolean('Add XLS export to accounting reports',
            help="""Installs the account_financial_report_webkit_xls module."""),
        'module_account_tax_analysis': fields.boolean('Tax analysis View',
            help="""Installs the account_tax_analysis module. Generate a menu under Accounting / Tax / Tax analysis you are able to group accounting entries by Taxes (VAT codes) and/or financial accounts."""),
        'module_account_clean_cancelled_invoice_number': fields.boolean('Allow canceled invoice number renumber and deletion',
            help="""Installs the account_clean_cancelled_invoice_number module. It adds a button on canceled invoice number so you can choose to remove internal number and then delete it or renumber by re-approving it."""),        
        'module_multi_store': fields.boolean('Manage a multi store environment with journals restrictions',
            help="""Installs the multi_store module. The main purpose of this module is to restrict journals access for users on different stores."""),
        'module_account_journal_active': fields.boolean('Allow journals activation/deactivation (adds field "active")',
            help="""Installs the account_journal_active module."""),
        'module_account_invoice_company_search': fields.boolean('Add to Invoice a filter by company and group by Company',
            help="""Installs the account_invoice_company_search module."""),
        
        # Sale / Purchase modules
        'module_purchase_discounts': fields.boolean('Mange disccounts on purchases',
            help="""Installs the purchase_discounts module."""),
        'module_sale_prices_update': fields.boolean('Add update system for sale order lines',
            help="""Installs the sale_prices_update module."""),
        'module_sale_order_validity': fields.boolean('Mange Sale Orders Validity',
            help="""Installs the sale_order_validity module."""),
        'module_sales_to_sale_order': fields.boolean('Add functionalty for grouping sales orders into a new sale order on other company',
            help="""Installs the sales_to_sale_order module."""),
        'module_portal_sale_distributor': fields.boolean('Create a portal group "distributors" and allow them to create and confirm sale orders',
            help="""Installs the module_portal_sale_distributor module."""),
        'module_sale_dummy_confirmation': fields.boolean('On a multi-company environment with stock and/or account, allow using only sale for some companies.',
            help="""Installs the sale_dummy_confirmation module."""),
        'module_sale_stock_availability': fields.boolean('See Stock availability in sales order line.',
            help="""Installs the sale_stock_availability module."""),
        'module_sale_restrict_partners': fields.boolean('Restrict see own leads partner to see their own partners only.',
            help="""Installs the sale_restrict_partners module."""),
        'module_sale_pricelist_discount': fields.boolean('See Pricelist Discount on Sales Orders.',
            help="""Installs the sale_pricelist_discount module."""),
        'module_price_security': fields.boolean('Restrict some users to edit prices or change pricelist on sales and partners.',
            help="""Installs the price_security module."""),
        'module_account_analytic_purchase_contract': fields.boolean('Manage contracts on Purchase.',
            help="""Installs the account_analytic_purchase_contract module."""),
        'module_account_analytic_analysis_mods': fields.boolean('Make some improovements on contracts managements.',
            help="""Installs the account_analytic_analysis_mods module. Basically:\
            * On creating invoice fill "reference" with contract name\
            * On creating invoice compute tax for total
            * On creating invoice take only tax of contract company
            """),
        
        # Project
        'module_project_issue_solutions': fields.boolean('Project Issue Solutions',
            help="""Installs the project_issue_solutions module."""),
        'module_project_alert_upcoming_tasks': fields.boolean('Alert upcoming task',
            help="""Installs the project_alert_upcoming_tasks module."""),
        'module_project_description': fields.boolean('Use description on projects',
            help="""Installs the project_description module."""),
        'module_project_issue_create_task_defaults': fields.boolean('Use issue task information on creating a task from an issue',
            help="""Installs the project_issue_create_task_defaults module."""),
        'module_project_issue_product': fields.boolean('Relate issues to products (and viceversa)',
            help="""Installs the project_issue_product module."""),
        'module_project_task_order': fields.boolean('Change default tasks order to "priority desc, sequence, date_deadline, planned_hours, date_start, create_date desc"',
            help="""Installs the project_task_order module."""),
        'module_project_issue_order': fields.boolean('Add sequence field to issues and change default order to "priority desc, sequence, date_deadline, duration, create_date desc"',
            help="""Installs the project_issue_order module."""),

        # Multi Company
        'module_web_easy_switch_company': fields.boolean('Multi company - Enable Company Easy Change',
            help="""Installs the web_easy_switch_company module."""),
        'module_inter_company_rules': fields.boolean('Manager inter company rules',
            help="""Installs the inter_company_rules module."""),
        'module_inter_company_move': fields.boolean('Manager inter company document move',
            help="""Installs the inter_company_move module."""),

        # Usability and tools modules
        'module_web_group_expand': fields.boolean('Allow group by lists to be expanded and collapased with buttons',
            help="""Installs the web_group_expand module."""),
        'module_help_doc': fields.boolean('Install Help Documentation',
            help="""Installs the help_doc module."""),
        'module_mass_editing': fields.boolean('Mass Editing',
            help="""Installs the mass_editing module."""),
        'module_currency_rate_update': fields.boolean('Update currencies rates automatically',
            help="""Installs the currency_rate_update module."""),
            # Not functional for now
        'module_web_export_view': fields.boolean('Web Export View. Export to csv',
            help="""Installs the web_export_view module."""),
        'module_visual_export': fields.boolean('Visual Export. Export to ods',
            help="""Installs the visual_export module."""),
        'module_web_printscreen_zb': fields.boolean('Web Printscreen. Export to pdf or to xls',
            help="""Installs the web_printscreen_zb module."""),
        
        # Technical
        'module_mail_local_server_catchall': fields.boolean('Configure catchall on local server',
            help="""Installs the mail_local_server_catchall module."""),
        'module_auth_admin_passkey': fields.boolean('Use admin password as a passkey for all active logins',
            help="""Installs the auth_admin_passkey module."""),
        'module_adhoc_support': fields.boolean('Use ADHOC support',
            help="""Installs the adhoc_support module."""),
        'module_cron_run_manually': fields.boolean('Enable Run Cron Manually',
            help="""Installs the cron_run_manually module."""),
        'module_disable_openerp_online': fields.boolean('Disable OpenERP Online',
            help="""Installs the disable_openerp_online module."""),

        # Partner modules
        'module_partner_person': fields.boolean('Add person information to partners.',
            help="""Installs the partner_person module. Add firstname, lastname, birthdate, etc."""),
        'module_partner_social_fields': fields.boolean('Add social fields to partners',
            help="""Installs the partner_social_fields module."""),
        'module_partner_user': fields.boolean('Add user quick creation from partners',
            help="""Installs the partner_user module."""),
        'module_base_state_active': fields.boolean('Hide USA states and add active field for states',
            help="""Installs the base_state_active module."""),
        'module_partner_views_fields': fields.boolean('Add Fields on Partners Views',
            help="""Installs the partner_views_fields module."""),
        'module_partner_search_by_ref': fields.boolean('Search Partners by Reference',
            help="""Installs the partner_search_by_ref module."""),
        'module_partner_search_by_vat': fields.boolean('Search Partners by VAT',
            help="""Installs the partner_search_by_vat module."""),
        'module_partner_state': fields.boolean('Manage different states on partners',
            help="""Installs the partner_state module."""),
        'module_partner_school': fields.boolean('Manage School Data on partners',
            help="""Installs the partner_school module."""),

        # Product modules
        'module_product_pack': fields.boolean('Mange product packs',
            help="""Installs the product_pack module."""),
        'module_product_pack_sale_order_warning': fields.boolean('Mange stock warnings on product packs',
            help="""Installs the product_pack_sale_order_warning module."""),
        'module_product_price_currency': fields.boolean('Manage different currencies on product sale price',
            help="""Installs the product_price_currency module."""),
        'module_product_dimensions': fields.boolean('Manage product dimmensions',
            help="""Installs the product_dimensions module."""),
        'module_product_supplier_pricelist': fields.boolean('Mange easier supplier pricelist',
            help="""Installs the product_supplier_pricelist module."""),
        'module_product_unique': fields.boolean('Validate product unicity per company on ean13 and interal reference fields',
            help="""Installs the product_unique module."""),
        'module_product_historical_price': fields.boolean('Historical price for product in a product tab',
            help="""Installs the product_historical_price module."""),
        'module_product_salesman_group': fields.boolean('Restrict salesman to see only authorized products by using salesman groups.',
            help="""Installs the product_salesman_group module."""),
        'module_product_uom_prices': fields.boolean('Allow to define different prices for different UOMs',
            help="""Installs the product_uom_prices module."""),
        'module_product_force_create_variants': fields.boolean('Allow to force create variants on product templates',
            help="""Installs the product_force_create_variants module."""),
    }        
    
    _defaults = {
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
