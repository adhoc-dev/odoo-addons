# -*- coding: utf-8 -*-
{
    'name': 'Stock Picking Locations',
    'version': '1.0',
    'category': 'Warehouse Management',
    'sequence': 14,
    'summary': '',
    'description': """
Stock Picking Locations
=======================
Add Location and Destiny Location to stock picking. When stock moves are
created they are taken by default.
Add a button to stock picking to update the stock move Location and Destiny
Location.
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'stock',
    ],
    'data': [
        'stock_view.xml',
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
