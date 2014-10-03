# -*- coding: utf-8 -*-


{
    'name': 'Location Security',
    'version': '1.0',
    'category': 'Warehouse Management',
    'sequence': 14,
    'summary': '',
    'description': """
Location Security
=================
Users can be assigned many Stock Journals and then they can be
restricted to see only this Journals.
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'stock', 
        'res_users_helper_functions',
    ],
    'data': [
        'res_users_view.xml',
        'stock_view.xml',
        'security/location_security_security.xml',
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