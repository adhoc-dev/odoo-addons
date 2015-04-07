# -*- coding: utf-8 -*-
from openerp import fields, models, api


class product_catalog_report(models.Model):
    _inherit = 'product.product_catalog_report'

    category_type = fields.Selection(
        [('public_category', 'Public Category'),
         ('accounting_category', 'Accounting Category')], 'Category Type',
        required=True
    )
    public_category_ids = fields.Many2many(
        'product.public.category',
        'product_catalog_report_categories_public',
        'product_catalog_report_id',
        'category_id',
        'Product Categories Public',
        required=True
    )

    @api.multi
    def generate_report(self):
        """ Print the catalog
        """
        self.ensure_one()

        context = self._context.copy()
        if self.category_type == 'public_category':
            category_ids = self.public_category_ids.ids
            if self.include_sub_categories:
                category_ids = self.env['product.public.category'].search(
                    [('id', 'child_of', category_ids)]).ids
        else:
            category_ids = self.category_ids.ids
            if self.include_sub_categories:
                category_ids = self.env['product.category'].search(
                    [('id', 'child_of', category_ids)]).ids

        context['category_ids'] = category_ids
        context['category_type'] = self.category_type
        context['product_type'] = self.product_type
        context['pricelist_ids'] = self.pricelist_ids.ids
        context['products_order'] = self.products_order
        context['categories_order'] = self.categories_order
        context['only_with_stock'] = self.only_with_stock

        return self.env['report'].with_context(context).get_action(
            self, self.report_xml_id.report_name)
