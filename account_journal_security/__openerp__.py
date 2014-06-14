# -*- coding: utf-8 -*-
{
    'name': 'Journal Security',
    'version': '1.0',
    'category': 'Accounting',
    'sequence': 14,
    'summary': '',
    'description': """
Journal Security
================
It creates a many2many field between journals and users. If you set users to journal or viceversa, then this journals and the related moves, will be only seen by selected users.
Usually used for payroll journals.
This fields are only seen by users with "access right management"
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'account',
        'account_voucher',
    ],
    'data': [
            'res_users_view.xml',
            'account_view.xml',
            'security/journal_security_security.xml',
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