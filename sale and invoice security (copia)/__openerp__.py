# -*- coding: utf-8 -*-
{
    'name': 'Partner State',
    'version': '1.0',
    'category': 'Base',
    'description': """
Partner State
=============
Agrega tres estados para los Clientes: 'Potencial', 'Pendiente de aprobación' y 'Aprobado'. Se requieren cierta información para poder pasar de un estado a otro. Info requerida
También se modifica el workflow de los Pedidos de ventas y facturas para que se puedan autorizar solo aquellos pedidos de clientes aprobados o de “consumidores finales” en donde el monto total sea inferior a $1000 y término de pago sea contado.
    """,
    'author': 'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'depends': [
        'base',
    ],
    'data': [
            'company_view.xml',
            'partner_view.xml',
            'security/partner_state_security.xml',
    ],
    'demo': [],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
