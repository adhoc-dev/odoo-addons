# -*- coding: utf-8 -*-


{
    'name': 'Sale Add Products Wizard',
    'version': '1.0',
    'category': 'Sales & Purchases',
    'sequence': 14,
    'summary': '',
    'description': """
Sale Add Products Wizard
==========================
This module adds a " multi Add " button on sales orders calling a wizard "sale order add multiple" 
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'sale',
    ],
    'data': [
        'wizard/sale_add_multiple.xml',
        'sale_view.xml'
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
