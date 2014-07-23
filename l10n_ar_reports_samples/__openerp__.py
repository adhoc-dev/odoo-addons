# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (C) 2012 OpenERP - Team de Localización Argentina.
# https://launchpad.net/~openerp-l10n-ar-localization
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name':     'Reportes de la localización argentina',
    'version':  '0.1',
    'author':   'OpenERP - Team de Localización Argentina',
    'category': 'Localization/Argentina',
    'website':  'https://launchpad.net/~openerp-l10n-ar-localization',
    'license':  'AGPL-3',
    'description': """Configura reportes de muestra para ordenes de venta, remitos, recibos y facturas según características típicas argentinas. La idea es que viendo como se usa y aprovechando esos templates cada uno lo configure a gusto.
IMPORTANTE:
Algunos reportes requieren algunos otros modulos que no los pusimos como dependencia porque en realidad uno puede querer modificar el reporte o tal vez no usar determinado reporte. 
* Recibos: 'l10n_ar_account_check_duo'
* Remitos: 'delivery_extension', 'stock_picking_print_sequence',

ATENCION: luego de instalar el modulo, es muy util entrar a los reportes de las facturas y agregar: 
* Salvar como prefijo para anexos: (object.state in ('open','paid')) and ('INV'+(object.number or '').replace('/','')+'.pdf')
* Recargar de anexo = True
* Se incluyen las plantillas de ilustrator para diseñar facturas, remitos y demás documentación según los templates implementados en este ejemplo. También se incluyen las fuentes utilizadas. Puede encontrar dicho material en /material

El módulo utiliza varias decencias que solo son necesarias porque los templates .odt que instala llaman a campos que se agregan con esas dependencias.

Los reportes que se configuran para mostrar funcionalidades son:

    o Presupuesto – Sin foto (sale.order)
        · Se imprime con fondo como si no se usase preimpreso
        · Imprime el título “Presupuesto”
        · Solo trabaja para sale.order en draft

    o Orden de compra – Con foto  (sale.order)
        · Se imprime con fondo como si no se usase preimpreso
        · Imprime el título “Orden de compra”
        · Solo trabaja para sale.order que no estén en draft

    o Remitos (stock.picking)
        · Se imprime con fondo solo para mostrar el fondo.
        · Tienen configurado imprimir garantía y lote

    o Factura. Configurada para imprimir en pre-impresos.
        · No imprime numero de factura
        · Tiene configurada 25 lineas por hoja. Si la factura tiene más líneas entonces la parte automáticamente generando una nueva factura.
        · No esta implementado todavía pero en la configuración de las facturas hay una opción para decir si se incluyen o no los impuestos en el precio (para facturas B por ejemplo) y hasta para seleccionar cuales serían los impuestos a incluir (serían los impuestos ‘IVA’)

    o Nota de crédito. Configurada como si fuese una nota de crédito electrónica o donde nosotros podemos asignar un número.
        · Imprime el número de factura
        · Imprime “hoja x de y” y no importa el número de ítems del invoice, no lo parte.
        · Imprime fondo, logo y demás
        · Usa otro template de facturas que muestra la descripción de una línea de la factura.

    Los módulos de los cuales depende este modulo ('delivery_extension','report_aeroo_generator' y 'stock_picking_print_sequence'), se encuentran en https://code.launchpad.net/~sistemas-adhoc/openobject-addons/addons.
    
    NOTA: Los reportes definidos en este modulo hacen uso de los módulos account_check, delivery_extension y stock_picking_print_sequence. Por lo tanto estos debe ser instalados para que los reportes funcionen bien.
""",
    'depends': [
        #'account_check',
        #'delivery_extension',
        'report_aeroo_generator',
        # 'l10n_ar_invoice',
        #'stock_picking_print_sequence',
    ],
    'init_xml': [],
    'demo_xml': [],
    'test': [],
    'update_xml': [
        'data/report_configuration_defaults_data.xml',
        'data/report_configuration.xml',
        'data/report_configuration_line.xml',
        'data/ir_sequence.xml',
    ],
    'active': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
