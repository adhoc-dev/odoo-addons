# -*- coding: utf-8 -*-
{'active': False,
    'author': 'Ingenieria ADHOC.',
    'category': 'base.module_category_knowledge_management',
    'demo_xml': [],
    'depends': [
        'sale',
        'product_price_currency',
        ],
    'description': """
Product UOM Prices
==================
* Add a o2m field on products to allow defining prices in different uoms
* Add a new type of price calculation on pricelists (for the new o2m field
    on products)
* Change domain on sale order lines so that only defined uoms can be choosen.

Video TUTORIAL: https://www.youtube.com/watch?v=-jGsbEZDOJE
""",
    'init_xml': [],
    'installable': True,
    'license': 'AGPL-3',
    'name': 'Product UOM Prices',
    'test': [],
    'update_xml': [
        'view/product_view.xml',
        'security/ir.model.access.csv',
    ],
    'version': 'No version',
    'website': ''}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
