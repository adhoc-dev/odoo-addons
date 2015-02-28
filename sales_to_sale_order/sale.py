# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp import SUPERUSER_ID, _
from openerp.exceptions import Warning


class sale_order(osv.osv):
    _inherit = 'sale.order'

    _columns = {
        'grouped_on_new_so': fields.boolean(
            'Grouped?',
            help="Grouped in new Sale Order?",
            readonly=True),
    }

    def copy_and_group_sale_orders(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        sale_obj = self
        saleline_obj = self.pool.get('sale.order.line')

        # Buscamos con SUPERUSER_ID por si no tiene permisos
        user_obj = self.pool['res.users']
        user = user_obj.browse(
            cr, SUPERUSER_ID, uid, context=context)
        new_user = user.new_sale_order_user_id
        # Volvemos a buscar al usuario pero con el id del nuevo usuario 
        # (para tener un contexto apropiado en los properties)
        new_user = user_obj.browse(cr, new_user.id, new_user.id, context=context)
        if not new_user:
            raise Warning(
                _('No new user configured. You must first set up a "New Sale Order User" for current user.')
                )
        new_user_id = new_user.id
        company = new_user.company_id

        new_user_partner = new_user.partner_id

        so_name = _('Grouped Sale Order')
        so_vals = self._so_vals(
            cr,
            new_user_id,
            so_name,
            new_user_partner,
            company,
            context=context)
        sale_id = sale_obj.create(cr, new_user_id, so_vals, context=context)

        so_lines = {}
        # so_lines = []
        # TODO  Las lineas que no tienen productos no las estamos llevando por
        # ahora
        for so in self.browse(cr, uid, ids, context=context):
            for so_line in so.order_line:
                if so_line.product_id:
                    if so_line.product_id.id not in so_lines:
                        so_lines[so_line.product_id.id] = {
                            'product': so_line.product_id,
                            'product_uom_qty': so_line.product_uom_qty,
                        }
                    else:
                        so_lines[so_line.product_id.id][
                            'product_uom_qty'] += so_line.product_uom_qty
                else:
                    so_lines['no_prod_line_' + str(so_line.id)] = {
                        'name': so_line.name,
                        'price': so_line.price_unit,
                        'product_uom_qty': so_line.product_uom_qty,
                        'product_uom': so_line.product_uom,
                    }
            # so_lines.extend(so.order_line)
        for line in so_lines:
            so_line_vals = self._so_line_vals_from_group(
                cr,
                new_user_id,
                so_lines[line],
                new_user_partner,
                company,
                sale_id,
                context=context)
            saleline_obj.create(cr, new_user_id, so_line_vals, context=context)

        # Write grouped_on_new_so = True
        self.write(cr, uid, ids, {'grouped_on_new_so': True}, context=context)
        return True

    def _so_line_vals_from_group(self, cr, uid, values, partner, company, sale_id, context=None):
        """ @ return : Sale Line values dictionary """
        if context is None:
            context = {}
        saleline_obj = self.pool.get('sale.order.line')
        tax_obj = self.pool.get('account.tax')

        taxes_ids = []
        sale = self.browse(cr, uid, sale_id, context=context)
        product = values.get('product', False)
        product_uom_qty = values.get('product_uom_qty', False)
        product_uom = values.get('product_uom', False)
        name = values.get('name', False)
        price = values.get('price', 0.0)
        if product:
            soline_onchange = saleline_obj.product_id_change(
                cr,
                uid,
                [],
                sale.pricelist_id.id,
                product.id,
                qty=product_uom_qty,
                uom=product.uom_id.id,
                partner_id=partner.id,
                context=context)
            if soline_onchange.get('value') and soline_onchange['value'].get('tax_id'):
                taxes_ids = soline_onchange['value']['tax_id']
            if soline_onchange.get('value'):
                if soline_onchange['value'].get('price_unit'):
                    price = soline_onchange['value'].get('price_unit')
        # Fetch taxes by company not by inter-company user
        company_taxes = [tax_rec.id for tax_rec in tax_obj.browse(
            cr,
            uid,
            # SUPERUSER_ID,
            taxes_ids,
            context=context
            ) if tax_rec.company_id.id == company.id]

        return {
            'name': product and product.name or name,
            'order_id': sale_id,
            'product_uom_qty': product_uom_qty,
            'product_id': product and product.id or False,
            'product_uom': product and product.uom_id.id or product_uom and product_uom.id,
            'price_unit': price,
            'company_id': company.id,
            'tax_id': [(6, 0, company_taxes)],
        }

    def _so_vals(self, cr, uid, name, partner, company, context=None):
        """ @ return : Sale values dictionary """
        if context is None:
            context = {}
        seq_obj = self.pool.get('ir.sequence')
        partner_obj = self.pool.get('res.partner')
        partner_addr = partner_obj.address_get(
            cr,
            uid,
            # SUPERUSER_ID,
            [partner.id],
            ['default', 'invoice', 'delivery', 'contact'])
        pricelist_id = partner.property_product_pricelist.id
        fpos = partner.property_account_position and partner.property_account_position.id or False
        # Not good but browse here for compatible code
        return {
            'name': seq_obj.get(cr, uid, 'sale.order') or '/',
            # 'name': seq_obj.get(cr, SUPERUSER_ID, 'sale.order') or '/',
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
