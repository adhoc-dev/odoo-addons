# -*- coding: utf-8 -*-
{
    'name': 'Stock Voucher',
    'version': '1.0',
    'category': 'Warehouse Management',
    'sequence': 14,
    'summary': '',
    'description': """
Stock Voucher
=============
Add stock voucher report on stock picking
TODO:
-----
* agregar el boton de enviar por email
* agregar constraints de company en stock.py
* que el reporte que se carga no sea el mismo del picking, nosotros no lo usamosportque terminamos usando uno de aeroo
    """,
    'author':  'ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'delivery',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/stock_print_remit_view.xml',
        'views/report_stockpicking.xml',
        'stock_view.xml',
        'stock_remit_data.xml',
        'stock_menu.xml',
        'views/views_templates.xml',
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
