# -*- coding: utf-8 -*-
from openerp import fields, models, api


class product_catalog_report(models.Model):
    _name = 'product.product_catalog_report'
    _description = 'Product Catalog Report with Aeroo'

    name = fields.Char(
        'Name',
        required=True
    )
    products_order = fields.Char(
        'Products Order Sintax',
        help='for eg. name desc', required=False
    )
    categories_order = fields.Char(
        'Categories Order Sintax',
        help='for eg. name desc',
    )
    include_sub_categories = fields.Boolean(
        'Include Subcategories?',
    )
    only_with_stock = fields.Boolean(
        'Only With Stock Products?',
    )
    print_product_uom = fields.Boolean(
        'Print Product UOM?',
        )
    product_type = fields.Selection(
        [('product.template', 'Product Template'),
         ('product.product', 'Product')], 'Product Type',
        required=True
    )
    prod_display_type = fields.Selection(
        [('prod_per_line', 'One Product Per Line'),
         ('prod_list', 'Product List'),
         ('variants', 'Variants'),
         ], 'Product Display Type',
    )
    report_xml_id = fields.Many2one(
        'ir.actions.report.xml',
        'Report XML',
        domain=[('report_type', '=', 'aeroo'),
                ('model', '=', 'product.product')],
        context={'default_report_type': 'aeroo',
                 'default_model': 'product.product'},
        required=True
    )
    category_ids = fields.Many2many(
        'product.category',
        'product_catalog_report_categories',
        'product_catalog_report_id',
        'category_id',
        'Product Categories',
    )
    pricelist_ids = fields.Many2many(
        'product.pricelist',
        'product_catalog_report_pricelists',
        'product_catalog_report_id',
        'pricelist_id',
        'Pricelist',
    )

    @api.multi
    def prepare_report(self):
        context = self._context.copy()
        category_ids = self.category_ids.ids
        if self.include_sub_categories:
            category_ids = self.env['product.category'].search(
                    [('id', 'child_of', category_ids)]).ids

        context['category_ids'] = category_ids
        context['product_type'] = self.product_type
        context['pricelist_ids'] = self.pricelist_ids.ids
        context['products_order'] = self.products_order
        context['categories_order'] = self.categories_order
        context['only_with_stock'] = self.only_with_stock
        context['prod_display_type'] = self.prod_display_type
        context['print_product_uom'] = self.print_product_uom
        return self.with_context(context)

    @api.multi
    def generate_report(self):
        """ Print the catalog
        """
        self.ensure_one()
        self = self.prepare_report()
        return self.env['report'].get_action(
            self, self.report_xml_id.report_name)
