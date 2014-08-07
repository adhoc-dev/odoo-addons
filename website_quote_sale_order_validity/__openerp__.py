# -*- coding: utf-8 -*-
{
    'name': 'Website Quoate Sale Order Validity',
    'version': '1.0',
    'category': 'Sales & Purchases',
    'sequence': 14,
    'summary': '',
    'description': """
Website Quoate Sale Order Validity
==================================
This modules rewrite validity_date field if website_quote is installed and you are using our custom module 'sale_order_validity'
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'sale_order_validity',
        'website_quote',
    ],
    'data': [
	 	'sale_order_view.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': True,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: