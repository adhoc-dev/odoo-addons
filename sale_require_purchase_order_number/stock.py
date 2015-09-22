# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api, _
from openerp.exceptions import Warning


class stock_picking(models.Model):
    _inherit = "stock.picking"

    @api.one
    @api.depends('group_id', 'sale_id')
    def _get_purchase_order_number(self):
        if self.manual_purchase_order_number:
            self.purchase_order_number = self.manual_purchase_order_number
        else:
            self.purchase_order_number = self.sale_id.purchase_order_number

    @api.one
    def _set_purchase_order_number(self):
        self.manual_purchase_order_number = self.purchase_order_number

    require_purchase_order_number = fields.Boolean(
        string='Sale Require Origin',
        related='partner_id.require_purchase_order_number')
    manual_purchase_order_number = fields.Char(
        'Purchase Order Number',
        states={'cancel': [('readonly', True)],
                'done': [('readonly', True)]})
    purchase_order_number = fields.Char(
        compute='_get_purchase_order_number',
        inverse='_set_purchase_order_number',
        string='Purchase Order Number',
        states={'cancel': [('readonly', True)],
                'done': [('readonly', True)]})
    code = fields.Selection(
        related='picking_type_id.code',
        string='Operation Type')

    @api.model
    def _get_invoice_vals(self, key, inv_type, journal_id, move):
        invoice_vals = super(stock_picking, self)._get_invoice_vals(
            key, inv_type, journal_id, move)
        invoice_vals.update({
            'purchase_order_number': move.picking_id.purchase_order_number})
        return invoice_vals

    @api.cr_uid_ids_context
    def do_enter_transfer_details(self, cr, uid, picking, context=None):
        for o in self.browse(cr, uid, picking):
            if o.require_purchase_order_number and o.code == 'outgoing':
                if not o.purchase_order_number:
                    raise Warning(_(
                        'You cannot transfer products without a Purchase Order Number for this partner'))
        return super(stock_picking, self).do_enter_transfer_details(cr, uid, picking, context=None)
