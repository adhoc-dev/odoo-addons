# -*- coding: utf-8 -*-
{
    'name': 'Stock Remit (depreciado)',
    'version': '1.0',
    'category': 'Warehouse Management',
    'sequence': 14,
    'summary': '',
    'description': """
Stock Remit (depreciado)
===========
Para que la asignacion del diario funcione bien (en funcion a la tienda de la sale.order), se debe verificar también el diario de encadenamiento configurado en las ubicaciones de stock (principalmente en salida)
    """,
    'author':  'ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'delivery',
        'report_extended_stock', #lo requiere para garantizar que se pase por contexto "remit"
    ],
    'data': [
        'wizard/stock_print_remit_view.xml',
        'stock_view.xml',
        'stock_remit_data.xml',
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
