# -*- coding: utf-8 -*-


{
    'name': 'Product Supplier Pricelist',
    'version': '1.0',
    'category': 'Product',
    'sequence': 14,
    'summary': '',
    'description': """
Product Supplier Pricelist
==========================
Add sql constraint to restrict:
1. That you can only add one supplier to a product per company
2. That you can add olny one record of same quantity for a supplier pricelist

It also adds to more menus (and add some related fields) on purchase/product. 
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'purchase',
    ],
    'data': [
        'product_view.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: