# -*- coding: utf-8 -*-


{
    'name': 'Project Member Create Tasks',
    'version': '1.0',
    'category': 'Projects & Services',
    'sequence': 14,
    'summary': '',
    'description': """
Project Member Create Tasks
===========================
Este modulo realiza las siguientes modificaciones:
* a los usuarios (permiso project/user o superior) que se agreguen como miembros en "proyectos", les permite crear editar y borrar tareas de ese proyecto. 
* Luego de creada la tarea, el usuario solo podra modificar algunos campos y tendra permisos limitados. 
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com.ar',
    'images': [
    ],
    'depends': [
        'project_security',
    ],
    'data': [
        'security/security.xml',
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