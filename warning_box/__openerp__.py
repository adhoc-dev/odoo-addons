# -*- coding: utf-8 -*-
{
    'name': "Warning box",
    'version': '0.1',
    'category': 'Tools',
    'description': """
        [ENG] Add Warning box.
        usage return self.pool.get('warning_box').info(cr, uid, title='The title', message='the message')
    """,
    'author': 'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'license': 'AGPL-3',
    "depends": ['base'],
    "data": ['warning_box.xml',
             ],
    "active": False,
    "installable": True
}
