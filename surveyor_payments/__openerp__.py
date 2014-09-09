# -*- coding: utf-8 -*-
{
    'name': 'Surveyor Payments',
    'version': '1.0',
    'category': 'Warehouse Management',
    'sequence': 14,
    'summary': '',
    'description': """
Surveyor Payments
=================
Allow to register payments on taks and give availability to track them.
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'project',
        'account',
    ],
    'data': [
        'project_task_view.xml',
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
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
