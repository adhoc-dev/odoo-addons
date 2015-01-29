# -*- coding: utf-8 -*-
from openerp import models, fields


class adhoc_base_configuration(models.TransientModel):
    _name = 'adhoc.base.config.settings'
    _inherit = 'res.config.settings'

    # Fixes
    module_account_voucher_multic_fix = fields.Boolean(
        'FiX voucher in multi-company father/son environment',
        help="""Installs the account_voucher_multic_fix module.""")
    module_account_multic_fix = fields.Boolean(
        'FiX account in multi-company father/son environment',
        help="""Installs the account_multic_fix module.""")
    module_sale_multic_fix = fields.Boolean(
        'FiX sale in multi-company father/son environment',
        help="""Installs the sale_multic_fix module.""")
    module_purchase_multic_fix = fields.Boolean(
        'FiX purchase in multi-company father/son environment',
        help="""Installs the purchase_multic_fix module.""")
    module_account_voucher_account_fix = fields.Boolean(
        'FIX vouchers credit/debit account choose. If payment, use credit account; if receipt, use debit account',
        help="""Installs the account_voucher_account_fix module.""")
    module_account_onchange_fix = fields.Boolean(
        'FIX account on changes in multicompany environment',
        help="""Installs the account_onchange_fix module.""")
    module_stock_multic_fix = fields.Boolean(
        'FIX invoice creation wizard from picking in multicompany environment',
        help="""Installs the stock_multic_fix module.""")

    # Account modules
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

    # Sale / Purchase modules
    module_sale_add_products_wizard = fields.Boolean(
        'Add a wizard to add multiple products on a sale order',
        help="""Installs the sale_add_products_wizard module.""")
    module_purchase_discount = fields.Boolean(
        'Mange disccounts on purchases',
        help="""Installs the purchase_discount module.""")
    module_sale_prices_update = fields.Boolean(
        'Add update system for sale order lines',
        help="""Installs the sale_prices_update module.""")
    module_sale_order_validity = fields.Boolean(
        'Mange Sale Orders Validity',
        help="""Installs the sale_order_validity module.""")
    module_sales_to_sale_order = fields.Boolean(
        'Add functionalty for grouping sales orders into a new sale order on other company',
        help="""Installs the sales_to_sale_order module.""")
    module_portal_sale_distributor = fields.Boolean(
        'Create a portal group "distributors" and allow them to create and confirm sale orders',
        help="""Installs the module_portal_sale_distributor module.""")
    module_sale_dummy_confirmation = fields.Boolean(
        'On a multi-company environment with stock and/or account, allow using only sale for some companies.',
        help="""Installs the sale_dummy_confirmation module.""")
    module_sale_stock_availability = fields.Boolean(
        'See Stock availability in sales order line.',
        help="""Installs the sale_stock_availability module.""")
    module_sale_restrict_partners = fields.Boolean(
        'Restrict see own leads partner to see their own partners only.',
        help="""Installs the sale_restrict_partners module.""")
    module_sale_pricelist_discount = fields.Boolean(
        'See Pricelist Discount on Sales Orders.',
        help="""Installs the sale_pricelist_discount module.""")
    module_price_security = fields.Boolean(
        'Restrict some users to edit prices or change pricelist on sales and partners.',
        help="""Installs the price_security module.""")
    module_account_analytic_purchase_contract = fields.Boolean(
        'Manage contracts on Purchase.',
        help="""Installs the account_analytic_purchase_contract module.""")
    module_partner_samples = fields.Boolean(
        'Manage Samples Given to Customers.',
        help="""Installs the partner_samples module.""")
    module_sale_multiple_invoice = fields.Boolean(
        'On Invoicing from sale order, adds an option to make multiple invoices by once.',
        help="""Installs the sale_multiple_invoice module.""")
    module_sale_other_product_description = fields.Boolean(
        'Add "Other Sale Description" field on Products.',
        help="""Installs the sale_other_product_description module. Add "Other Sale Description" field on Products. If this field is set,
then on sale orders lines this description will be used and no code""")
    module_account_analytic_analysis_mods = fields.Boolean(
        'Make some improovements on contracts managements.',
        help="""Installs the account_analytic_analysis_mods module. Basically:\
            * On creating invoice fill "reference" with contract name\
            * On creating invoice compute tax for total
            * On creating invoice take only tax of contract company
            """)
    module_purchase_uom_prices_uoms = fields.Boolean(
        'Restrict purchase uom to the product uom, purchase product uom and uoms defined in UOM Prices.',
        help="""Installs the purchase_uom_prices_uoms.""")
    module_sale_contract_restrict_domain = fields.Boolean(
        'Restrict contracts/projects on sales order to contract and same partner or no partner set.',
        help="""Installs the sale_contract_restrict_domain.""")
    module_crm_partner_history = fields.Boolean(
        'Adds CRM partner history page on partners form view as it exists on odoo v6.1.',
        help="""Installs the crm_partner_history.""")
    module_purchase_double_validation_imp = fields.Boolean(
        'Adds a button for confirmed orders so that you can print the purchase order.',
        help="""Installs the purchase_double_validation_imp module.""")
    module_sale_contract_editable = fields.Boolean(
        'Sale Contract Restrict Domain.',
        help="""Installs the sale_contract_editable module.""")
    module_sale_require_contract = fields.Boolean(
        'Require a Contract on Sale Order Confirmation.',
        help="""Installs the sale_require_contract module.""")
    module_sale_require_ref = fields.Boolean(
        'Require a Reference on Sale Order Confirmation.',
        help="""Installs the sale_require_ref module.""")
    module_purchase_usability_extension = fields.Boolean(
        'Display Invoices and Incoming Shipments on Purchase Order form view (in dedicated tabs).',
        help="""Installs the purchase_usability_extension module.""")
    module_sale_line_product_required = fields.Boolean(
        'Product becomes a required field on sale order lines.',
        help="""Installs the sale_line_product_required module.""")
    module_sale_usability_extension = fields.Boolean(
        'Display Invoices and Delivery Orders on Sale Order form view (in dedicated tabs).',
        help="""Installs the sale_usability_extension module.""")

    # Project
    module_project_issue_solutions = fields.Boolean(
        'Project Issue Solutions',
        help="""Installs the project_issue_solutions module.""")
    module_project_alert_upcoming_tasks = fields.Boolean(
        'Alert upcoming task',
        help="""Installs the project_alert_upcoming_tasks module.""")
    module_project_description = fields.Boolean(
        'Use description on projects',
        help="""Installs the project_description module.""")
    module_project_issue_create_task_defaults = fields.Boolean(
        'Use issue task information on creating a task from an issue',
        help="""Installs the project_issue_create_task_defaults module.""")
    module_project_issue_product = fields.Boolean(
        'Relate issues to products (and viceversa)',
        help="""Installs the project_issue_product module.""")
    module_project_task_order = fields.Boolean(
        'Change default tasks order to "priority desc, sequence, date_deadline, planned_hours, date_start, create_date desc"',
        help="""Installs the project_task_order module.""")
    module_project_issue_order = fields.Boolean(
        'Add sequence field to issues and change default order to "priority desc, sequence, date_deadline, duration, create_date desc"',
        help="""Installs the project_issue_order module.""")
    module_project_task_issues = fields.Boolean(
        'Add Issue in to task view',
        help="""Installs the project_task_issues module.""")
    module_project_tags = fields.Boolean(
        'Add Tags on Projects',
        help="""Installs the project_tags module.""")
    module_project_task_desc_html = fields.Boolean(
        'Changes description type on tasks to html',
        help="""Installs the project_task_desc_html module.""")
    module_project_task_phase = fields.Boolean(
        'Add project phases to tasks',
        help="""Installs the project_task_phase module.""")
    module_project_task_portal_unfollow = fields.Boolean(
        'Add functionality "not add to the task supporters of the project that do not have the activated field employee"',
        help="""Installs the project_task_portal_unfollow module.""")
    module_project_task_phase = fields.Boolean(
        'Add project phases to tasks',
        help="""Installs the project_task_phase module.""")
    module_project_user_story = fields.Boolean(
        'Project User Stories.',
        help="""Installs the project_user_story module.""")

    # Stock
    module_stock_picking_labels = fields.Boolean(
        'Add a picking label doc report on stock picking',
        help="""Installs the stock_picking_labels module.""")
    module_stock_picking_list = fields.Boolean(
        'Add an xls picking list report on stock picking',
        help="""Installs the stock_picking_list module.""")
    module_stock_picking_locations = fields.Boolean(
        'Allow changing stock locations globaly from picking',
        help="""Installs the stock_picking_locations module.""")
    module_stock_voucher = fields.Boolean(
        'Add stock voucher report on stock picking.',
        help="""Installs the module_stock_voucher module.""")
    module_stock_display_destination_move = fields.Boolean(
        'Display the field Destination Move in the Stock Move form view for Stock Managers in read-only. Very usefull for advanced users and debug purposes.',
        help="""Installs the stock_display_destination_move module.""")
    module_stock_display_sale_id = fields.Boolean(
        'Display the link to the sale order in the Delivery Order form view.',
        help="""Installs the stock_display_sale_id module.""")
    module_stock_cancel = fields.Boolean(
        'Allow you to bring back a completed stock picking to draft state',
        help="""Installs the stock_cancel module.""")
    module_stock_picking_invoice_link = fields.Boolean(
        'Add a link between pickings and generated invoices.',
        help="""Installs the stock_picking_invoice_link module.""")
    module_picking_dispatch = fields.Boolean(
        'Allow you to group various pickings into a dispatch order ,having all the related moves in it and assigned to a warehouse keeper.',
        help="""Installs the picking_dispatch module.""")
    module_stock_display_src_location = fields.Boolean(
        'Display the source location on the tree view of the move lines of the pickings (by default, only the destination location is displayed).',
        help="""Installs the stock_display_src_location module.""")
    module_stock_invoice_try_again = fields.Boolean(
        'When the sale order has "Create Invoice" set to "On Delivery Order", add a button "Create Invoice" on the Delivery Order once the goods are shipped.',
        help="""Installs the stock_invoice_try_again module.""")

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

    # Usability and tools modules
    module_web_recipients_uncheck = fields.Boolean(
        'Uncheck recipients on res.partner',
        help="""Installs the web_recipients_uncheck module.""")
    module_web_sheet_full_width = fields.Boolean(
        'Use the whole available screen width when displaying sheets',
        help="""Installs the web_sheet_full_width module.""")
    module_web_ckeditor4 = fields.Boolean(
        'Provides a widget for editing HTML fields using CKEditor 4.x',
        help="""Installs the module_web_ckeditor4 module.""")
    module_web_group_expand = fields.Boolean(
        'Allow group by lists to be expanded and collapased with buttons',
        help="""Installs the web_group_expand module.""")
    module_document_url = fields.Boolean(
        'Allow to attach an URL as a document.',
        help="""Installs the document_url module.""")
    module_help_doc = fields.Boolean(
        'Install Help Documentation',
        help="""Installs the help_doc module.""")
    module_mass_editing = fields.Boolean(
        'Mass Editing',
        help="""Installs the mass_editing module.""")
    module_help_online = fields.Boolean(
        'Allows the creation of an online help available from the lists and forms in Odoo.',
        help="""Installs the help_online module.""")
    module_currency_rate_update = fields.Boolean(
        'Update currencies rates automatically',
        help="""Installs the currency_rate_update module.""")
    module_evaluation = fields.Boolean(
        'Extends the functionality of the survey module in order to make assessments that are corrected automatically.',
        help="""Installs the evaluation module.""")
    module_web_m2x_options = fields.Boolean(
        'Modifies "many2one" and "many2manytags" form widgets so as to add some new display control options.',
        help="""Installs the web_m2x_options module.""")

    # Not functional for now
    module_web_export_view = fields.Boolean(
        'Web Export View. Export to csv',
        help="""Installs the web_export_view module.""")
    module_attachment_preview = fields.Boolean(
        'The module adds a little print preview icon right of download links for attachments or binary fields',
        help="""Installs the attachment_preview module.""")
    module_document_url = fields.Boolean(
        'Module that allows to attach an URL as a document.',
        help="""Installs the document_url module.""")

    # Technical
    module_auth_admin_passkey = fields.Boolean(
        'Use admin password as a passkey for all active logins',
        help="""Installs the auth_admin_passkey module.""")
    module_adhoc_support = fields.Boolean(
        'Use ADHOC support',
        help="""Installs the adhoc_support module.""")
    module_cron_run_manually = fields.Boolean(
        'Enable Run Cron Manually',
        help="""Installs the cron_run_manually module.""")
    module_disable_openerp_online = fields.Boolean(
        'Disable OpenERP Online',
        help="""Installs the disable_openerp_online module.""")

    # Partner modules
    module_partner_person = fields.Boolean(
        'Add person information to partners.',
        help="""Installs the partner_person module. Add firstname, lastname, birthdate, etc.""")
    module_partner_social_fields = fields.Boolean(
        'Add social fields to partners',
        help="""Installs the partner_social_fields module.""")
    module_base_state_active = fields.Boolean(
        'Hide USA states and add active field for states',
        help="""Installs the base_state_active module.""")
    module_partner_views_fields = fields.Boolean(
        'Add Fields on Partners Views',
        help="""Installs the partner_views_fields module.""")
    module_partner_search_by_ref = fields.Boolean(
        'Search Partners by Reference',
        help="""Installs the partner_search_by_ref module.""")
    module_partner_search_by_vat = fields.Boolean(
        'Search Partners by VAT',
        help="""Installs the partner_search_by_vat module.""")
    module_partner_state = fields.Boolean(
        'Manage different states on partners',
        help="""Installs the partner_state module.""")
    module_partner_school = fields.Boolean(
        'Manage School Data on partners',
        help="""Installs the partner_school module.""")
    module_partner_credit_limit = fields.Boolean(
        'Restrict credit limit edition on partners and restrict sale orders approval for partners without credit',
        help="""Installs the partner_credit_limit module.""")

    # Product modules
    module_product_pack = fields.Boolean(
        'Mange product packs',
        help="""Installs the product_pack module.""")
    module_product_price_currency = fields.Boolean(
        'Manage different currencies on product sale price',
        help="""Installs the product_price_currency module.""")
    module_product_dimensions = fields.Boolean(
        'Manage product dimmensions',
        help="""Installs the product_dimensions module.""")
    module_product_supplier_pricelist = fields.Boolean(
        'Mange easier supplier pricelist',
        help="""Installs the product_supplier_pricelist module.""")
    module_product_unique = fields.Boolean(
        'Validate product unicity per company on ean13 and interal reference fields',
        help="""Installs the product_unique module.""")
    module_product_historical_price = fields.Boolean(
        'Historical price for product in a product tab',
        help="""Installs the product_historical_price module.""")
    module_product_salesman_group = fields.Boolean(
        'Restrict salesman to see only authorized products by using salesman groups.',
        help="""Installs the product_salesman_group module.""")
    module_product_uom_prices = fields.Boolean(
        'Allow to define different prices for different UOMs',
        help="""Installs the product_uom_prices module.""")
    module_product_force_create_variants = fields.Boolean(
        'Allow to force create variants on product templates',
        help="""Installs the product_force_create_variants module.""")
    module_product_variant_imp = fields.Boolean(
        'Make Some Improovements in Variants and Attributes management',
        help="""Installs the product_variant_imp module.""")
    module_product_prices_update = fields.Boolean(
        'Update prices for the products',
        help="""Installs the product_prices_update.""")
    module_product_catalog_aeroo_report = fields.Boolean(
        'Report Product catalog.',
        help="""Installs the product_catalog_aeroo_report module.""")
    module_product_customer_price = fields.Boolean(
        'Product Costumer Prices.',
        help="""Installs the product_customer_price module.""")
    module_product_website_categ_search = fields.Boolean(
        'Product Search by Website Category.',
        help="""Installs the product_website_categ_search module.""")
    module_product_variant_csv_import = fields.Boolean(
        'Add a menu entry in *Sales > Configuration > Product Categories and attributes > Product Template CSV Import".',
        help="""Installs the product_variant_csv_import module.""")
    module_partner_products_shortcut = fields.Boolean(
        'Adds a shortcut on supplier partner form to the products supplied by this partner.',
        help="""Installs the partner_products_shortcut module.""")
    module_product_no_translation = fields.Boolean(
        'Set the translatable fields of the product object (name,descriptions) to non-translatable fields.',
        help="""Installs the product_no_translation module.""")
