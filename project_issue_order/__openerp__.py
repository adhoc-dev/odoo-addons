# -*- coding: utf-8 -*-
{
    'name': 'Project Issue Order',
    'version': '1.0',
    'category': 'Projects & Services',
    'sequence': 14,
    'summary': '',
    'description': """
Project Issue Order
===================
Add sequence field to issues and change default order to the following criteria:
    "priority desc, sequence, date_deadline, duration, create_date desc"
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'project_issue',
    ],
    'data': [
        'project_issue_view.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}