# -*- coding: utf-8 -*-
from openerp import models, fields


class adhoc_base_configuration(models.TransientModel):
    _inherit = 'adhoc.base.config.settings'

    # Fixes
    module_sale_multic_fix = fields.Boolean(
        'FiX sale in multi-company father/son environment',
        help="""Installs the sale_multic_fix module.""")

    # Sale modules
    module_sale_add_products_wizard = fields.Boolean(
        'Add a wizard to add multiple products on a sale order',
        help="""Installs the sale_add_products_wizard module.""")
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
    module_sale_multiple_invoice = fields.Boolean(
        'On Invoicing from sale order, adds an option to make multiple invoices by once.',
        help="""Installs the sale_multiple_invoice module.""")
    module_sale_other_product_description = fields.Boolean(
        'Add "Other Sale Description" field on Products.',
        help="""Installs the sale_other_product_description module. Add "Other Sale Description" field on Products. If this field is set,
then on sale orders lines this description will be used and no code""")
    module_sale_contract_restrict_domain = fields.Boolean(
        'Restrict contracts/projects on sales order to contract and same partner or no partner set.',
        help="""Installs the sale_contract_restrict_domain.""")
    module_crm_partner_history = fields.Boolean(
        'Adds CRM partner history page on partners form view as it exists on odoo v6.1.',
        help="""Installs the crm_partner_history.""")
    module_sale_contract_editable = fields.Boolean(
        'Sale Contract Restrict Domain.',
        help="""Installs the sale_contract_editable module.""")
    module_sale_require_contract = fields.Boolean(
        'Require a Contract on Sale Order Confirmation.',
        help="""Installs the sale_require_contract module.""")
    module_sale_require_ref = fields.Boolean(
        'Require a Reference on Sale Order Confirmation.',
        help="""Installs the sale_require_ref module.""")
    module_sale_line_product_required = fields.Boolean(
        'Product becomes a required field on sale order lines.',
        help="""Installs the sale_line_product_required module.""")
    module_sale_usability_extension = fields.Boolean(
        'Display Invoices and Delivery Orders on Sale Order form view (in dedicated tabs).',
        help="""Installs the sale_usability_extension module.""")
    module_sale_contract_default = fields.Boolean(
        'Concatenating the name of the contract with the name of the Partner',
        help="""Installs the sale_contract_default module.""")
