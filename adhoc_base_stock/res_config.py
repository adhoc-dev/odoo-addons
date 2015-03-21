# -*- coding: utf-8 -*-
from openerp import models, fields


class adhoc_base_configuration(models.TransientModel):
    _inherit = 'adhoc.base.config.settings'

    # Fixes
    module_stock_multic_fix = fields.Boolean(
        'FIX invoice creation wizard from picking in multicompany environment',
        help="""Installs the stock_multic_fix module.""")

    # Stock
    module_stock_picking_partner_editable = fields.Boolean(
        'Make Partner Editable on Confirmed Stock Pickings',
        help="""Installs the stock_picking_partner_editable module.""")
    module_product_stock_location = fields.Boolean(
        'Filter by locations on product view to see product stock in specified location',
        help="""Installs the product_stock_location module.""")
    module_stock_warehouse_edit = fields.Boolean(
        'Make Stock Warehouse Editable',
        help="""Installs the stock_warehouse_edit module. It allow to change locations linked to a warehouse. Used when you have to fix a migration or something similar. After use it is recommended to uninstall it.""")
    module_stock_inventory_negative_line = fields.Boolean(
        'Give availability to define negative stocks on a inventory',
        help="""Installs the stock_inventory_negative_line module.""")
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
    module_stock_move_defaults = fields.Boolean(
        'Set defaults values on stock moves in order to facilitate file import.',
        help="""Installs the stock_move_defaults module.""")
