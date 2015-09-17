# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api, _
from openerp.exceptions import Warning


class sale_order(models.Model):
    _inherit = "sale.order"

    require_purchase_order_number = fields.Boolean(
        string='Sale Require Origin',
        related='partner_id.require_purchase_order_number')
    purchase_order_number = fields.Char(
        'Purchase Order Number')

    def action_wait(self, cr, uid, ids, context=None):
        for o in self.browse(cr, uid, ids):
            if o.require_purchase_order_number:
                if not o.purchase_order_number:
                    raise Warning(_(
                        'You cannot confirm a sales order without a Purchase Order Number for this partner'))
        return super(sale_order, self).action_wait(cr, uid, ids, context)

    @api.model
    def _prepare_invoice(self, order, lines):
        invoice_vals = super(sale_order, self)._prepare_invoice(order, lines)
        invoice_vals.update({
            'purchase_order_number': order.purchase_order_number})
        return invoice_vals
