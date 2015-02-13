# -*- coding: utf-8 -*-
from openerp import models, fields, api


class account_invoice_prices_update(models.TransientModel):
    _name = 'account_invoice_update'

    @api.model
    def _get_pricelist(self):
        invoice_id = self._context.get('active_id', False)
        if invoice_id:
            invoice = self.env['account.invoice'].browse(invoice_id)
            if invoice.type in ('out_invoice', 'out_refund'):
                return invoice.partner_id.property_product_pricelist
            else:
                return invoice.partner_id.property_product_pricelist_purchase

    pricelist_id = fields.Many2one(
        'product.pricelist', string="Price List",
        required=True, default=_get_pricelist)

    @api.one
    def update_prices(self):
        active_id = self._context.get('active_id', False)
        invoice = self.env['account.invoice'].browse(active_id)
        invoice.write({'currency_id': self.pricelist_id.currency_id.id})
        for line in invoice.invoice_line:
            price = self.pricelist_id.price_get(
                line.product_id.id, line.quantity or 1.0,
                partner=line.partner_id.id,
                context={'uom': line.uos_id.id})[self.pricelist_id.id]
            line.price_unit = price
        return True
