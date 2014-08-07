# -*- coding: utf-8 -*-
{
    'name' : 'Sale Dummy Confirmation',
    'version': '1.0',
    'author': 'Ingenieria ADHOC',
    'website': 'www.ingenieria.com.ar',
    'depends' : ["sale"],
    'category' : 'Sale Management',
    'description': '''
Sale Dummy Confirmation
=======================
On a multi-company environment with stock and/or account, allow using only sale for some companies.
    ''',
    'init_xml' : [],
    'demo_xml' : [
    ],
    'update_xml' : [
        'company_view.xml',
        'sale_view.xml',
        ],
    'active': False,
    'installable': True
}
