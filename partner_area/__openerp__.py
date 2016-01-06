# -*- coding: utf-8 -*-
{
    'name': 'Partner Area',
    'version': '8.0.0.0.0',
    'category': 'Tools',
    'sequence': 14,
    'summary': '',
    'description': """
Partner Area
===========================

    """,
    'author':  'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'license': 'AGPL-3',
    'images': [
    ],
    'depends': [
        'base',
    ],
    'data': [
        'view/res_partner_view.xml',
        'partner_areas_menu.xml',
        'security/ir.model.access.csv',
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
