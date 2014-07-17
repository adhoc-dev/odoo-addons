# -*- coding: utf-8 -*-
# Renombrado porque el modulo document_page todavia existe pero sin contenido
{
    'name': 'Document Page',
    'version': '1.0.1',
    'category': 'Knowledge Management',
    'description': """
Pages
=====
Web pages
    """,
    'author': ['OpenERP SA'],
    'website': 'http://www.openerp.com/',
    'depends': ['knowledge'],
    'data': [
        'wizard/document_page_create_menu_view.xml',
        'wizard/document_page_show_diff_view.xml',
        'document_page_view.xml',
        'security/document_page_security.xml',
        'security/ir.model.access.csv',
    ],
    'demo': ['document_page_demo.xml'],
    'test': ['test/document_page_test00.yml'],
    'installable': True,
    'auto_install': False,
    'images': [],
    'css' : ['static/src/css/document_page.css'],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
