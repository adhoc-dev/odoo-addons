# -*- coding: utf-8 -*-
{
    'name': 'Product Catalog Aeroo Report',
    'version': '1.0',
    'category': 'Aeroo Reporting',
    'sequence': 14,
    'summary': '',
    'description': """
Product Catalog Aeroo Report
============================
    """,
    'author':  'Sistemas ADHOC',
    'website': 'www.sistemasadhoc.com.ar',
    'images': [
    ],
    'depends': [
        'product',
        'report_aeroo',
    ],
    'data': [
        'wizard/product_catalog_wizard.xml',
        'security/ir.model.access.csv',
        'product_catalog.xml',
        'report/product_catalog_view.xml'
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
