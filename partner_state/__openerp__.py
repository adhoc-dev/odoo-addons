# -*- coding: utf-8 -*-
{
    'name': 'Partner State',
    'version': '1.0',
    'category': 'Base',
    'description': """
Partner State
=============
Agrega tres estados para los Clientes: 'Potencial', 'Pendiente de aprobación' y 'Aprobado'. Se requieren cierta información para poder pasar de un estado a otro. Dicha información es configurable desde cada compañía.
Además, se configura en la compania si:
* Se quiere utilizar partner state en esa cia
* se quiere restringuir la aprobacion de ordenes de venta en esa cia con y sin limites de montos
    """,
    'author': 'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'depends': [
        'base',
        'sale',
    ],
    'data': [
        'company_view.xml',
        'partner_view.xml',
        'security/partner_state_security.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
