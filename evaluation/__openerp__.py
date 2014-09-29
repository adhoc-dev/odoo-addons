# -*- coding: utf-8 -*-



{   'active': False,
    'author': u'Ingenieria ADHOC',
    'category': u'base.module_category_knowledge_management',
    'demo_xml': [],
    'depends': ['survey',],
    'description': u"""
Extends the functionality of the survey module in order to make assessments that are corrected automatically
""",
    'init_xml': [],
    'installable': True,
    'license': 'AGPL-3',
    'name': u'Academic Evaluations',
    'test': [
            ],
    'data': [
            'view/survey_view.xml',
            'security/ir.model.access.csv',
            'security/survey_security.xml',
            ],
    'version': u'1.0',
    'website': 'www.ingadhoc.com'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
