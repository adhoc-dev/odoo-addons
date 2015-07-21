# -*- coding: utf-8 -*-
{
    'name':     'MRP auto production',
    'version':  '0.1',
    'author':   'ADHOC',
    'category': 'Localization/Argentina',
    'website':  'www.adhoc.com.ar',
    'license':  'AGPL-3',
    'description': """
Para probar instalar tambien "sale" y "procurement_jit_stock"
""",
    'depends': [
        'mrp',
        'procurement_jit_stock',
    ],
    'demo': [
        # TODO to fix data to pass test
        # 'mrp_demo.xml',
        ],
    'test': [],
    'data': [
        'mrp_view.xml',
    ],
    'active': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
