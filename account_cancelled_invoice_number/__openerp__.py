# -*- coding: utf-8 -*-
##############################################################################
#
#    Ingenieria ADHOC - ADHOC SA
#    https://launchpad.net/~ingenieria-adhoc
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Cancelled Invoice Number',
    'version': '1.0',
    'category': 'Accounting',
    'sequence': 14,
    'summary': 'Invoicing, Number, Cancelled',
    'description': """
Cancelled Invoice Number
========================
Modifica las vistas de las invoice para mostrar el número de facturas canceladas.

En primera instancia se intentó modificiar el campo "number" de account_invoice para que sea calculado de otra manera:
'number': fields.related('internal_number', type='char', readonly=True, size=64, store=True, string='Number'),
El problema es que, al validar una invoice:
    Primero se crea el asiento asginando un número, se completa automáticamnete number (tomando desde sequence)
    Luego se hace que invoice_number sea igual a number
    uien da el nombre a un asiento y no al revés. 


Se deja el archivo "analisis_account_cancel.csv" con analisis realizado sobre account_cancel
Si llega a ser deseable poder borrar facturas canceladas, se podria hacer editable el campo "internal number" para un determinado grupo de usuario, este usuario podria borrar dichos numeros y luego borrar la factura.
Tambien se puede analizar el modulo "nan_account_invoice_sequence"

ATENCION: se deben modificar los reportes deseados para que impriman "internal_number" en vez de "number"
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'account_cancel'
    ],
    'data': [
        'account_invoice_view.xml',
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