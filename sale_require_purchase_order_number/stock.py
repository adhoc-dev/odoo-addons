# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api


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

    @api.model
    def _get_invoice_vals(self, key, inv_type, journal_id, move):
        invoice_vals = super(stock_picking, self)._get_invoice_vals(
            key, inv_type, journal_id, move)
        invoice_vals.update({
            'purchase_order_number': move.picking_id.purchase_order_number})
        return invoice_vals
