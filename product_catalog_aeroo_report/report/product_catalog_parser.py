import time
from tools.translate import _

from report import report_sxw
from report.report_sxw import rml_parse

class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        
        self.lang = context.get('lang', 'es_ES')

        pricelist_ids = context.get('pricelist_ids')
        if pricelist_ids:
            product_obj = self.pool.get('product.pricelist')
            pricelists = product_obj.browse(cr, uid, pricelist_ids, context=context)
            if pricelists and not isinstance(pricelists, list):
                pricelists = [pricelists]
        else:
            pricelists = []
               
        category_ids = context['category_ids']
        categories_order = context.get('categories_order', '')
        self.category_ids = self.pool.get('product.category').search(self.cr, self.uid, [('id', 'in', category_ids)], order = categories_order, context=context)        
        self.categories = self.pool.get('product.category').browse(self.cr, self.uid, self.category_ids, context=context)
        if not isinstance(self.categories, list):
            self.categories = [self.categories]
        
        self.products = self.get_products(self.category_ids, context=context)
        if not isinstance(self.products, list):
            self.products = [self.products]

        company_id = self.pool.get('res.users').browse(cr, uid, [uid])[0].company_id         
        
        self.localcontext.update({
            'lang': self.lang,
            'categories': self.categories,
            'products': self.products,
            'company_logo': company_id.logo,
            'pricelists': pricelists,
            'today': time.localtime(),
            'get_price': self.get_price,       
            'get_products':self.get_products,     
        })

    def get_price(self, product, pricelist):
        context = {'pricelist': pricelist.id}
        product_obj = self.pool.get('product.product')
        price = product_obj._product_price(self.cr, self.uid, [product.id], False, False, context=context)
        return price.get(product.id, 0.0)        
    
    def get_products(self, category_ids, context=None):
        if not isinstance(category_ids, list):
            category_ids = [category_ids]

        template_ids = self.pool.get('product.template').search(self.cr, self.uid, [('categ_id', 'in', category_ids)], context=context)
        if not isinstance(template_ids, list):
            template_ids = [template_ids]        

        order= ''
        if context:
            order = context.get('products_order')

        # TODO: al pasar la funcion get_products desde el reporte no se ordenan los productos
        
        product_ids = self.pool.get('product.product').search(self.cr, self.uid, [('product_tmpl_id', 'in', template_ids),], order=order, context=context)
        print product_ids
        products = self.pool.get('product.product').browse(self.cr, self.uid, product_ids, context=context)
        return products
        # TODO filtrasr por productos o no en stock (opcional)