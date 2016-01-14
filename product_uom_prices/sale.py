# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api, SUPERUSER_ID


class sale_order_line(models.Model):

    """"""

    _inherit = 'sale.order.line'

    uom_unit_ids = fields.Many2many('product.uom', compute='_get_units')

    @api.one
    @api.depends('product_id')
    def _get_units(self):
        self.uom_unit_ids = self.get_product_uoms(self.product_id)

    @api.model
    def get_product_uoms(self, product):
        return product.uom_price_ids.mapped('uom_id') + product.uom_id

    @api.multi
    def product_id_change(
            self, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False,
            fiscal_position=False, flag=False):
        # because sale_stock module delete uom when colling this method, we
        # add it in context con module 'sale_stock_product_uom_prices'
        if not uom:
            uom = self._context.get('preserve_uom', False)
        res = super(sale_order_line, self).product_id_change(
            pricelist, product, qty=qty, uom=uom,
            qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
            lang=lang, update_tax=update_tax, date_order=date_order,
            packaging=packaging, fiscal_position=fiscal_position,
            flag=flag)

        if product:
            context_partner = {'lang': lang, 'partner_id': partner_id}
            product = self.env['product.product'].with_context(
                context_partner).browse(
                product)
            if (
                    not uom and product.use_uom_prices and
                    self.env.user.company_id.default_uom_prices
                    ):
                uom_id = product.uom_price_ids[0].uom_id.id
                res['value'].update(
                    {'product_uom': uom_id})

                # TODO REMOVE. we leave all this just in case we need
                # si tenemos instalado el modulo "sale_stock", entonces odoo
                # por defecto hace un hack y borrar la uom elegida y a uom y
                # precio por defecto del producto en nuestro caso entonces
                # termina quedando mal porque cambiamos la uom pero no el
                # precio por eso forzamos el recalculo del precio
                # price = self.env['product.pricelist'].browse(
                #     pricelist).with_context(
                #         uom=uom_id, date=date_order,).price_get(
                #         product.id, qty or 1.0, partner_id)[pricelist]
                # if price:
                #     if self.env.uid == SUPERUSER_ID and self._context.get(
                #             'company_id'):
                #         taxes = product.taxes_id.filtered(
                #             lambda r: r.company_id.id == self._context[
                #                 'company_id'])
                #     else:
                #         taxes = product.taxes_id
                #     price = self.env['account.tax']._fix_tax_included_price(
                #         price, taxes, res.get('value').get('tax_id'))
                #     res['value'].update({'price_unit': price})
            # we do this because odoo overwrite view domain
            if 'domain' not in res:
                res['domain'] = {}
            res['domain']['product_uom'] = [
                ('id', 'in', self.get_product_uoms(
                    product).ids)]
        return res
