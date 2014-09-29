# -*- coding: utf-8 -*-


{
    'name': 'Purchase Order Lines With Discounts',
    'version': '1.0',
    'category': 'Sales & Purchases',
    'sequence': 14,
    'summary': '',
    'description': """
Purchase Order Lines With Discounts
===================================
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
		"purchase", 
		"stock",
    ],
    'data': [
		"purchase_discount_view.xml", 
		"purchase_discount_report.xml",
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