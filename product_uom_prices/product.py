# -*- coding: utf-8 -*-
from openerp import models, fields, _, api
import openerp.addons.decimal_precision as dp
from openerp.exceptions import Warning


class product_uom_price(models.Model):

    """"""

    _name = 'product.uom.price'
    _description = 'Product Uom Price'

    product_tmpl_id = fields.Many2one(
        'product.template',
        string='Product Template',
        required=True,)
    uom_id = fields.Many2one('product.uom', string='UOM', required=True,)
    price = fields.Float(
        'Price', digits_compute=dp.get_precision('Price'),
        help="Sale Price for this UOM.")

    _sql_constraints = [
        ('price_uniq', 'unique(product_tmpl_id, uom_id)',
            'UOM mast be unique per Product Template!'),
    ]


class product_template(models.Model):

    """"""

    _inherit = 'product.template'

    use_uom_prices = fields.Boolean(
        'Use UOM Prices?',
        help='Use different prices for different UOMs?')
    uom_category_id = fields.Many2one(
        'product.uom.categ',
        string='UOM Category', related='uom_id.category_id')
    uom_price_ids = fields.One2many(
        'product.uom.price', 'product_tmpl_id', string='UOM Prices')

    @api.one
    @api.constrains('uom_price_ids')
    def _check_uoms(self):
        uom_ids = [x.uom_id.category_id.id for x in self.uom_price_ids]
        uom_ids = list(set(uom_ids))
        if len(uom_ids) > 1 or uom_ids[0] != self.uom_id.category_id.id:
            raise Warning(_('UOM Prices Category must be of the same \
                UOM Category as Product Unit of Measure'))

    def _price_get(self, cr, uid, products, ptype='list_price', context=None):
        res = super(product_template, self)._price_get(
            cr, uid, products, ptype=ptype, context=context)
        product_uom_price_obj = self.pool['product.uom.price']
        for product in products:
            if product.use_uom_prices and 'uom' in context:
                product_uom_price_ids = product_uom_price_obj.search(
                    cr, uid, [
                        ('uom_id', '=', context['uom']),
                        ('product_tmpl_id', '=', product.product_tmpl_id.id)],
                    context=context)
                if product_uom_price_ids:
                    res[product.id] = product_uom_price_obj.browse(
                        cr, uid, product_uom_price_ids[0],
                        context=context).price
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
