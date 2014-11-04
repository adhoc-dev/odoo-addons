# -*- coding: utf-8 -*-
{'active': False,
    'author': 'Ingenieria ADHOC.',
    'category': 'base.module_category_knowledge_management',
    'demo_xml': [],
    'depends': [
        'purchase',
        'product_uom_prices',
        ],
    'description': """
Purchase UOM Prices
==================
* Add a o2m field on products to allow defining prices in different uoms
* Add a new type of price calculation on pricelists (for the new o2m field
    on products)
* Change domain on purchase order lines so that only defined uoms can be choosen.

""",
    'init_xml': [],
    'installable': True,
    'license': 'AGPL-3',
    'name': 'Purchase UOM Prices',
    'test': [],
    'update_xml': [
    ],
    'version': 'No version',
    'website': 'www.ingadhoc.com'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
