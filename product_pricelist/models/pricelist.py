# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api, _
from openerp.exceptions import Warning
import openerp.addons.decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)


class product_pricelist(models.Model):
    _inherit = 'product.pricelist'

    price = fields.Float(
        string='Price',
        compute='_get_price',
        digits=dp.get_precision('Product Price'),
        help='Price for product specified on the context',
        )

    @api.one
    # TODO make multi
    def _get_price(self):
        product_id = self._context.get('product_id', False)
        template_id = self._context.get('template_id', False)
        if product_id:
            price = self.env['product.product'].browse(
                product_id).with_context(pricelist=self.id).price
            self.price = price
        elif template_id:
            price = self.env['product.template'].browse(
                template_id).with_context(pricelist=self.id).price
            self.price = price

    @api.multi
    def action_related_pricelist_items(self):
        self.ensure_one()
        product_id = self._context.get('product_id', False)
        template_id = self._context.get('template_id', False)
        onle_related_product_items = self._context.get(
            'onle_related_product_items', False)
        domain = [
            ('price_version_id.pricelist_id', '=', self.id),
            ]
        if onle_related_product_items:
            if product_id:
                product = self.env['product.product'].browse(product_id)
                domain += [
                    '|',
                    '|',
                    '|',
                    ('product_id', '=', product.id),
                    '&',
                    ('product_id', '=', False),
                    ('product_tmpl_id', '=', product.product_tmpl_id.id),
                    '&',
                    ('product_id', '=', False),
                    '&',
                    ('product_tmpl_id', '=', False),
                    ('categ_id', '=', product.categ_id.id),
                    '&',
                    ('product_id', '=', False),
                    '&',
                    ('product_tmpl_id', '=', False),
                    ('categ_id', '=', False),
                    ]
            elif template_id:
                template = self.env['product.template'].browse(template_id)
                domain += [
                    '|',
                    '|',
                    '&',
                    ('product_id', '=', False),
                    ('product_tmpl_id', '=', template.id),
                    '&',
                    ('product_id', '=', False),
                    '&',
                    ('product_tmpl_id', '=', False),
                    ('categ_id', '=', template.categ_id.id),
                    '&',
                    ('product_id', '=', False),
                    '&',
                    ('product_tmpl_id', '=', False),
                    ('categ_id', '=', False),
                    ]
        related_items = self.env['product.pricelist.item'].search(domain)
        name = _('Pricelist Items')
        new_context = self._context.copy()
        new_context['show_version'] = True
        new_context['pricelist_id'] = self.id
        res = {
            'name': name,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'res_model': 'product.pricelist.item',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'domain': [('id', 'in', related_items.ids)],
            'context': new_context,
            }
        return res
