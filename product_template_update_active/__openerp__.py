# -*- coding: utf-8 -*-
{'active': False,
    'author': 'Ingenieria ADHOC.',
    'category': 'base.module_category_knowledge_management',
    'demo_xml': [],
    'depends': ['product'],
    'description': """
Product Template Update Active Field
====================================

Update active field of product template in this way:
* If any related product product to this template has active = True, set True
* If all related product product to this template has active = False, set False
""",
    'init_xml': [],
    'installable': True,
    'license': 'AGPL-3',
    'name': u'Product Template Update Active Field',
    'test': [],
    'update_xml': [
        'wizard/product_template_update_active_field_view.xml',
    ],
    'website': 'www.ingadhoc.com'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
