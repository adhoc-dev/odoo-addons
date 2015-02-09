# -*- coding: utf-8 -*-
{
    'name': 'Stock availability in sales order line',
    'version': '0.1',
    'category': 'Tools',
    'description': """
Stock availability in sales order line
======================================
* Add two groups. One for seeing stock on sale orders and other to see only if or not available
* Add an option in warehouse to disable stock warning

IMPORTANT:
----------
    * This module could break some warnings as the ones implemented by "warning" module
    * If you dont disable warning and give a user availbility to see only "true/false" on sale order stock, he can see stock if the warning is raised
    """,
    'author': 'Moldeo Interactive & Ingenieria Adhoc',
    'website': 'http://business.moldeo.coop http://ingadhoc.com/',
    'images': [],
    'depends': [
        'sale_stock'
    ],
    'demo': [],
    'data': [
        'sale_view.xml',
        'stock_view.xml',
        'security/sale_order.xml',
        ],
    'test': [],
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
