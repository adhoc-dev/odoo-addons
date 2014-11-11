# -*- coding: utf-8 -*-
from openerp.osv import osv, fields


class account_invoice_prices_update(osv.osv_memory):
    _name = 'account_invoice_update'

    _columns = {
        'pricelist_id': fields.many2one(
            'product.pricelist', string="Price List"),
    }

    _defaults = {
        'pricelist_id': lambda s, cr, u, c: s.pool.get('res.users').browse(
            cr, u, u, c).partner_id.property_product_pricelist.id,
    }

    def update_prices(self, cr, uid, ids, context=None):
        context = context or {}
        active_id = context.get('active_id', False)
        invoice_line_obj = self.pool.get('account.invoice.line')
        partner_id = self.pool.get('res.users').browse(cr, uid, uid).partner_id
        wizard = self.browse(cr, uid, ids[0], context=context)
        if not wizard.pricelist_id:
            return {}
        invoice_line = self.pool['account.invoice'].browse(
            cr, uid, active_id, context=context).invoice_line
        for line in invoice_line:
            price = self.pool.get('product.pricelist').price_get(
                cr, uid, [wizard.pricelist_id.id],
                line.product_id.id, line.quantity or 1.0, partner_id.id, {
                    'uom': line.uos_id.id,
                })[wizard.pricelist_id.id]
            invoice_line_obj.write(cr, uid, [line.id], {'price_unit': price})
        return True
