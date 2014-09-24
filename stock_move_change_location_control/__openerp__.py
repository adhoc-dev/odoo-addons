# -*- coding: utf-8 -*-


{
    'name': 'Stock Move Change Location Control',
    'version': '1.0',
    'category': 'Warehouse Management',
    'sequence': 14,
    'summary': '',
    'description': """
Stock Move Change Location Control
==================================
If the location of a stock move is changed when it is the state Ready to Process,
then the state of that move is changed to Waiting Availability.
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'stock',
    ],
    'data': [
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

