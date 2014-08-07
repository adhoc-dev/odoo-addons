# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp import SUPERUSER_ID, _
from openerp.exceptions import except_orm, Warning, RedirectWarning

class sale_order(osv.osv):
    _inherit = 'sale.order'

    def copy_and_group_sale_orders(self, cr, uid, ids, context=None):        
        if context is None:
            context = {}
        company_obj = self.pool.get('res.company')
        sale_obj = self
        saleline_obj = self.pool.get('sale.order.line')

        # Buscamos con SUPERUSER_ID por si no tiene permisos
        user = self.pool['res.users'].browse(cr, SUPERUSER_ID, uid, context=context)
        new_user = user.new_sale_order_user_id
        if not new_user:
            raise Warning(_('No new user configured. You must first set up a "New Sale Order User" for current user.'))
        new_user_id = new_user.id
        company = new_user.company_id

        new_user_partner = new_user.partner_id
        
        so_name = _('Grouped Sale Order')
        so_vals = self._so_vals(cr, new_user_id, so_name, new_user_partner, company, context=context)
        sale_id = sale_obj.create(cr, new_user_id, so_vals, context=context)

        so_lines = []
        for so in self.browse(cr, uid, ids, context=context):
            so_lines.extend(so.order_line)
        for line in so_lines:
            so_line_vals = self._so_line_vals(cr, new_user_id, line, new_user_partner, company, sale_id, context=context)
            saleline_obj.create(cr, new_user_id, so_line_vals, context=context)
        return True

    def _so_line_vals(self, cr, uid, line, partner, company, sale_id, context=None):
        """ @ return : Sale Line values dictionary """
        if context is None:
            context = {}
        saleline_obj = self.pool.get('sale.order.line')
        tax_obj = self.pool.get('account.tax')

        #It may not affected because of parallel company relation
        taxes_ids = [x.id for x in line.tax_id]
        price = line.price_unit or 0.0
        sale = self.browse(cr, uid, sale_id, context=context)
        if line.product_id:
            soline_onchange = saleline_obj.product_id_change(cr, uid, [], sale.pricelist_id.id, line.product_id.id, qty=line.product_uom_qty,
            uom = line.product_id.uom_id.id, partner_id=partner.id, context=context)
            if soline_onchange.get('value') and soline_onchange['value'].get('tax_id'):
                taxes_ids = soline_onchange['value']['tax_id']
            if soline_onchange.get('value'):
                if soline_onchange['value'].get('price_unit'):
                    price = soline_onchange['value'].get('price_unit')
        #Fetch taxes by company not by inter-company user
        company_taxes = [tax_rec.id for tax_rec in tax_obj.browse(cr, SUPERUSER_ID, taxes_ids, context=context) if tax_rec.company_id.id == company.id]

        return {
            'name': line.product_id and line.product_id.name or line.name,
            'order_id': sale_id,
            'product_uom_qty': line.product_uom_qty,
            'product_id': line.product_id and line.product_id.id or False,
            'product_uom': line.product_id and line.product_id.uom_id.id or line.product_uom.id,
            'price_unit': price,
            'delay': line.product_id and line.product_id.sale_delay or 0.0,
            'company_id': company.id,
            'tax_id': [(6, 0, company_taxes)],
        }

    def _so_vals(self, cr, uid, name, partner, company, context=None):
    # def _so_vals(self, cr, uid, name, purchase_id, partner, company, direct_delivery_address, context=None):
        """ @ return : Sale values dictionary """
        if context is None:
            context = {}
        seq_obj = self.pool.get('ir.sequence')
        partner_obj = self.pool.get('res.partner')
        partner_addr = partner_obj.address_get(cr, SUPERUSER_ID, [partner.id], ['default', 'invoice', 'delivery', 'contact'])
        pricelist_id = partner.property_product_pricelist.id
        fpos = partner.property_account_position and partner.property_account_position.id or False
        #Not good but browse here for compatible code
        return {
            'name': seq_obj.get(cr, SUPERUSER_ID, 'sale.order') or '/',
            'company_id': company.id,
            'client_order_ref': name,
            'partner_id': partner.id,
            'pricelist_id': pricelist_id,
            'partner_invoice_id': partner_addr['invoice'],
            'date_order': fields.datetime.now(),
            'fiscal_position': fpos,
            'user_id': False,
            'auto_generated': True,
        }
