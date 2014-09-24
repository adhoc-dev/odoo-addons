# -*- coding: utf-8 -*-


{
    'name': 'Project Issue Solutions',
    'version': '1.0',
    'category': 'Projects & Services',
    'sequence': 14,
    'summary': '',
    'description': """
Project Issue Solutions
=======================
Add new object call solutions and adds a m2o field from issues to solutions
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com.ar',
    'images': [
    ],
    'depends': [
        'project_issue',
    ],
    'data': [
        'project_issue_view.xml',
        'project_issue_solution_view.xml',
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
