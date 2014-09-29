# -*- coding: utf-8 -*-


{
    'name': 'Project Tags',
    'version': '1.0',
    'category': 'Projects & Services',
    'sequence': 14,
    'summary': '',
    'description': """
Project Tags
============
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com.ar',
    'images': [
    ],
    'depends': [
        'project_security',
    ],
    'data': [
      'security/project_tags_group.xml',
      'view/project_view.xml',
      'view/project_tag_view.xml',
      'view/project_tags_menuitem.xml',
      'data/project_properties.xml',
      'data/project_tag_properties.xml',
      'data/project_track.xml',
      'data/project_tag_track.xml',
      'security/ir.model.access.csv'
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