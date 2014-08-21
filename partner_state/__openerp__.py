# -*- coding: utf-8 -*-
{
    'name': 'Partner State',
    'version': '1.0',
    'category': 'Base',
    'description': """
Partner State
=============
Agrega tres estados para los Clientes: 'Potencial', 'Pendiente de aprobación' y 'Aprobado'. Se crea un workflow para transiciónar entre estos 3 estados y se requieren cierta información para poder pasar de un estado a otro. Info requerida
- Domicilio de facturación o por defecto con todos su datos
- Posición fiscal 
- Plazo de pago
- Cuit
- Listas de precios
- 1 Categoría
- Comercial y equipo de ventas
- 1 adjunto denominado “constancia.pdf”
También se modifica el workflow de los Pedidos de ventas y facturas para que se puedan autorizar solo aquellos pedidos de clientes aprobados o de “consumidores finales” en donde el monto total sea inferior a $1000 y término de pago sea contado.
    """,
    'author': 'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'depends': ['sale', 'crm', 'base_vat', 'res_users_helper_functions'],
    'init_xml': [],
    'update_xml': [
            'partner_view.xml',
            'partner_workflow.xml',
            # 'invoice_view.xml', Vamos a revisar si esta vista la tenemos que poner o no
            'sale_view.xml',
            'security/partner_state_security.xml',
            'partner_on_install.xml',],
    'demo_xml': [],
    'test':[],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
