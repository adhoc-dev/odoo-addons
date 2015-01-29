# -*- coding: utf-8 -*-
from openerp.osv import fields, osv


class product_catalog(osv.osv_memory):
    _name = 'product_catalog'
    _description = 'Wizard to generate the Product Catalog Report with Aeroo'

    _columns = {
        'product_catalog_report_id': fields.many2one('product.product_catalog_report', 'Product Catalog', required=True),
    }

    _defaults = {
    }

    def generate_report(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids)[0]

        catalog = wizard.product_catalog_report_id
        if not catalog:
            return {'type': 'ir.actions.act_window_close'}

        return self.pool.get('product.product_catalog_report').generate_report(cr, uid, [catalog.id], context)
