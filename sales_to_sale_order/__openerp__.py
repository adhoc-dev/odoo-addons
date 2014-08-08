# -*- coding: utf-8 -*-
{
    'name' : 'Sales to Sale Order',
    'version': '1.0',
    'author': 'Ingenieria ADHOC',
    'website': 'www.ingenieria.com.ar',
    'depends' : ["sale"],
    'category' : 'Sale Management',
    'description': '''
Sales to Sale Order
===================
This module create a wizard asociated to an action on Sale
Orders. This wizard generates a Sale Order in another company for all sale orders items.
    ''',
    'demo' : [
        'portal_demo.xml',
    ],
    'data' : [
        'security/sales_t_sale_order_security.xml',
        'wizard/sales_to_sale_order_wizard_view.xml',
        'res_users_view.xml',
        'sale_view.xml',
        ],
    'active': False,
    'installable': True
}
