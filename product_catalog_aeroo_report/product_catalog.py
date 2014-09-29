# -*- coding: utf-8 -*-


from osv import fields, osv
from tools.translate import _

class product_catalog_report(osv.osv):
    _name = 'product.product_catalog_report'
    _description = 'Product Catalog Report with Aeroo'


    _columns = {
        'name': fields.char('Name', required=True),
        'products_order': fields.char('Products Order Sintax', help='for eg. name desc', required=False),
        'categories_order': fields.char('Categories Order Sintax', help='for eg. name desc', required=False),
        'report_xml_id': fields.many2one('ir.actions.report.xml', 'Report XML', domain="[('report_type','=','aeroo'),('model','=','product.product')]", context="{'default_report_type': 'aeroo', 'default_model': 'product.product'}", required=True),
        'category_ids': fields.many2many('product.category', 'product_catalog_report_categories','product_catalog_report_id', 'category_id', 'Product Categories', required=True),
        'pricelist_ids': fields.many2many('product.pricelist', 'product_catalog_report_pricelists', 'product_catalog_report_id', 'pricelist_id', 'Pricelist', required=False),
    }

    _defaults = {
    }
    

    def generate_report(self, cr, uid, ids, context=None):
        for report in self.browse(cr, uid, ids):
        
            categories = report.category_ids
            if not categories:
                return {'type': 'ir.actions.act_window_close'}
            if not isinstance(categories, list):
                categories = [categories]
            context['category_ids'] = map(lambda cat: cat.id, categories)
            
            pricelist_ids = report.pricelist_ids
            if not pricelist_ids:
                pricelist_ids = []
            if not isinstance(pricelist_ids, list):
                pricelist_ids = [pricelist_ids]
            
            context['pricelist_ids'] = map(lambda lst: lst.id, pricelist_ids)

            context['products_order'] = report.products_order
            context['categories_order'] = report.categories_order

            report_product_catalog = self.pool.get('ir.actions.report.xml').browse(cr, uid, [report.report_xml_id.id])[0].report_name

            result = {'type' : 'ir.actions.report.xml',
                      'context' : context,
                      'report_name': report_product_catalog,}
        return result


