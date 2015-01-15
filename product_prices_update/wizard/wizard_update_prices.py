# -*- coding: utf-8 -*-
from openerp import fields, models, api, _
from openerp.exceptions import Warning
from openerp import tools


class prices_update_wizard(models.TransientModel):
    _name = 'product.prices_update_wizard'

    price_type = fields.Selection(
        [('list_price', 'Sale Price'), ('standard_price', 'Cost Price')],
        required=True,
        string='Price Type')
    price_discount = fields.Float('Price Discoun')
    price_surcharge = fields.Float(
        'Price Surcharge', help='Specify the fixed amount to add or substract(if negative) to the amount calculated with the discount.')
    price_round = fields.Float('Price Rounding', help="Sets the price so that it is a multiple of this value.\n"
                               "Rounding is applied after the discount and before the surcharge.\n"
                               "To have prices that end in 9.99, set rounding 10, surcharge -0.01"
                               )
    check = fields.Boolean('Check before changing')

    @api.multi
    def change_prices(self, context=None):
        active_ids = context.get('active_ids', [])
        products_vals = []
        if not active_ids:
            raise Warning(_('You must select at least one product'))
        if self.check is True:
            actions = self.env.ref(
                'product_prices_update.action_prices_update_wizard_result')
            if actions:
                action_read = actions.read()[0]
                action_read['context'] = {
                    'product_tmpl_ids': active_ids,
                    'price_type': self.price_type,
                    'price_discount': self.price_discount,
                    'price_surcharge': self.price_surcharge,
                    'price_round': self.price_round,
                }
                return action_read
        else:
            for prodct in self.env['product.template'].browse(
                    active_ids):
                if self.price_type == 'list_price':
                    old_price = prodct.list_price
                elif self.price_type == 'standard_price':
                    old_price = prodct.standard_price
                else:
                    raise Warning(
                        _('Price type "%s" is not implemented') % (self.price_type))
                new_price = self.calc_new_price(
                    old_price, self.price_discount,
                    self.price_surcharge, self.price_round)
                vals = {
                    'product_tmpl': prodct,
                    'new_price': new_price,
                }
                products_vals.append(vals)
            return self.update_prices(products_vals, self.price_type)

    @api.model
    def update_prices(self, products_vals, price_type):
        product_ids = []
        for line in products_vals:
            line['product_tmpl'].write({price_type: line['new_price']})
            product_ids.append(line['product_tmpl'].id)
        return {
            'type': 'ir.actions.act_window',
            'name': _('Products'),
            'res_model': 'product.template',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', product_ids)],
            'target': 'current',
            'nodestroy': True,
        }

    @api.model
    def calc_new_price(
            self, old_price, price_discount, price_surcharge, price_round):
        new_price = old_price * \
            (1.0 + (price_discount or 0.0))
        if price_round:
            new_price = tools.float_round(
                new_price, precision_rounding=price_round)
        if price_surcharge:
            new_price += price_surcharge
        return new_price


class prices_update_wizard_result_detail(models.TransientModel):
    _name = 'product.prices_update_wizard_result_detail'

    result_id = fields.Many2one(
        'product.prices_update_wizard_result', 'Result')
    product_tmpl_id = fields.Many2one(
        'product.template', 'Product Template',
        readonly=True)
    old_price = fields.Float(
        'Old Price',
        readonly=True)
    new_price = fields.Float(
        'New Price',
        required=True
    )


class prices_update_wizard_result(models.TransientModel):
    _name = 'product.prices_update_wizard_result'

    @api.model
    def _get_details(self):
        ret = []
        price_discount = self._context.get('price_discount', 0.0)
        price_surcharge = self._context.get('price_surcharge', 0.0)
        price_round = self._context.get('price_round', 0.0)
        product_tmpl_ids = self._context.get('product_tmpl_ids', [])
        price_type = self._context.get('price_type', False)
        for product_tmpl in self.env['product.template'].browse(
                product_tmpl_ids):
            if price_type == 'list_price':
                old_price = product_tmpl.list_price
            elif price_type == 'standard_price':
                old_price = product_tmpl.standard_price
            else:
                raise Warning(
                    _('Price type "%s" is not implemented') % (price_type))
            vals = {
                'product_tmpl_id': product_tmpl.id,
                'old_price': old_price,
                'new_price': self.env[
                    'product.prices_update_wizard'].calc_new_price(
                    old_price, price_discount,
                    price_surcharge, price_round),
            }
            ret.append(vals)
        return ret

    detail_ids = fields.One2many(
        'product.prices_update_wizard_result_detail',
        'result_id',
        string='Products Detail',
        default=_get_details,
    )

    @api.multi
    def confirm(self):
        products_vals = []
        price_type = self._context.get('price_type', False)
        for line in self.detail_ids:
            vals = {
                'product_tmpl': line.product_tmpl_id,
                'new_price': line.new_price,
            }
            products_vals.append(vals)
        return self.env['product.prices_update_wizard'].update_prices(
            products_vals, price_type)
