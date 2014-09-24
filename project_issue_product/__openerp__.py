# -*- coding: utf-8 -*-


{
    'name': 'Project Issue Product',
    'version': '1.0',
    'category': 'Projects & Services',
    'sequence': 14,
    'summary': '',
    'description': """
Project Issue Product
=====================
Adds product field on Issues (M2O) and issue field on products (O2M)
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com.ar',
    'images': [
    ],
    'depends': [
        'project_issue',
        'product',
    ],
    'data': [
        'project_issue_view.xml',
        'product_view.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}