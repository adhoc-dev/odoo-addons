# -*- coding: utf-8 -*-


{
    'name': 'Project and Analytic Account integration impprovements',
    'version': '1.0',
    'category': 'Projects & Services',
    'sequence': 14,
    'summary': '',
    'description': """
Project and Analytic Account integration impprovements.
=======================================================

Adds domains restriction to project task so that only projets that use task and are not in cancelled, done or tempalte state, can be choosen. 
Adds domains restriction to timesheet records so that only
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com.ar',
    'images': [
    ],
    'depends': [
        'project_timesheet',
        'hr_timesheet_invoice',
    ],
    'data': [
        'project_timesheet_view.xml',       
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