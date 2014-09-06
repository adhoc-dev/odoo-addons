# -*- coding: utf-8 -*-
from openerp import fields, models, api


class account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'

    @api.multi
    def _get_user_restrict_prices(self):
        self.user_restrict_prices = self.env[
            'res.users'].restrict_prices

    user_restrict_prices = fields.Boolean(
        compute='_get_user_restrict_prices',
        string='User Restrict Prices')
    product_can_modify_prices = fields.Boolean(
        related='product_id.can_modify_prices',
        string='Product Can modify prices')

    def onchange_price_unit(self, cr, uid, ids, price_unit):
        return {'value': {'price_unit_copy': price_unit}}

    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        print 'self', self
        if self.invoice_id.type in ['out_invoice', 'out_refund']:
            self.check_discount_constrains(vals)
        return super(account_invoice_line, self).create(vals)

    @api.multi
    def write(self, vals):
        for line in self:
            if line.invoice_id.type in ['out_invoice', 'out_refund']:
                line.check_discount_constrains(vals)
        return super(account_invoice_line, self).write(vals)

    @api.model
    def check_discount_constrains(self, vals):
        discount = vals.get('discount', False)
        print 'discount', discount
        # pricelist = self.get_invoice_pricelist(
        #     cr, uid, line_id, vals, context=context)

        # if discount:
        #     restriction_obj = self.pool.get(
        #         'price_security.discount_restriction')
        #     restriction_obj.check_discount_with_restriction(
        #         cr, uid, discount, pricelist.id, context=context)


    def get_invoice_pricelist(self, cr, uid, line_id, vals, context=None):
        pricelist = False

        invoice_id = vals.get('invoice_id', False)

        if invoice_id:
            invoice_obj = self.pool.get('account.invoice')
            invoice = invoice_obj.browse(cr, uid, invoice_id, context=context)
            if isinstance(invoice, list):
                invoice = invoice[0]
            if invoice.partner_id.property_product_pricelist:
                pricelist = invoice.partner_id.property_product_pricelist
        elif line_id:
            line_obj = self.pool.get('account.invoice.line')
            line = line_obj.browse(cr, uid, line_id, context=context)
            if isinstance(line, list):
                line = line[0]
            if line.invoice_id.partner_id.property_product_pricelist:
                pricelist = line.invoice_id.partner_id.property_product_pricelist
# for case when creating invice from sale order
        else:
            partner_obj = self.pool.get('res.partner')
            partner = partner_obj.browse(
                cr, uid, vals.get('partner_id', False), context=context)
            if isinstance(partner, list):
                partner = partner[0]
            if partner.property_product_pricelist:
                pricelist = partner.property_product_pricelist
        return pricelist

    def product_id_change(self, cr, uid, ids, product, uom, qty=0, name='', type='out_invoice', partner_id=False,
                          fposition_id=False, price_unit=False, address_invoice_id=False, currency_id=False, context=None,
                          company_id=None):
        ret = super(account_invoice_line, self).product_id_change(cr, uid, ids, product, uom, qty=qty, name=name, type=type,
                                                                  partner_id=partner_id, fposition_id=fposition_id, price_unit=price_unit, address_invoice_id=address_invoice_id,
                                                                  currency_id=currency_id, context=context, company_id=company_id)

        if not product:
            return ret

        product_obj = self.pool.get('product.product')
        product = product_obj.browse(cr, uid, product, context=context)
        if isinstance(product, list):
            product = product[0]

        group_obj = self.pool.get('res.groups')
        if group_obj.user_in_group(cr, uid, uid, 'price_security.can_modify_prices', context=context):
            ret['value']['user_can_modify_prices'] = True
        else:
            ret['value']['user_can_modify_prices'] = False

        if product.can_modify_prices:
            ret['value']['product_can_modify_prices'] = True
        else:
            ret['value']['product_can_modify_prices'] = False

        return ret