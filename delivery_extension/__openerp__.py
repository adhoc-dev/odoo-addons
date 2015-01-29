# -*- coding: utf-8 -*-
{
    'name': 'Delivery Extension (depreciado)',
    'version': '1.0',
    'category': 'Warehouse Management',
    'sequence': 14,
    'summary': '',
    'description': """
Delivery Extension (depreciado)
==================
Add a field declared_value to Stock Picking that contains the declared valued.
It also adds to Stock Picking the address of the carrier.
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'delivery',
    ],
    'data': [
        'stock_view.xml'
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': False,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
