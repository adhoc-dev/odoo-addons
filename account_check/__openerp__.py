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
    'name': 'Account Check Management',
    'version': '1.0',
    'category': 'Accounting',
    'sequence': 14,
    'summary': 'Accounting, Payment, Check, Third, Issue',
    'description': """
Account Check Management
========================

TODO: multicurrency
-------------------
La segunda pregunta esta asociado al deposito del cheque, es porque la moneda principal de mi empresa es USD, pero hay cobros que se hacen en una segunda moneda , y cuando deposito un cheque en esa otra moneda hace el apunte como si lo que estuviera depositando fueran USD. 

Ejemplo (los asientos los pongo en una imagen que adjunto)
Un cliente me paga 1 000 000 PYG por una factura de 216 USD
Al validar el pago hace el asiento 1 de la imagen
Al depositar el cheque hace el asiento 2 de la imagen, cosa que no esta bien, lo correcto es algo parecido al primer asiento, porque en realidad son 216 usd, no 1 000 000 usd, y con ese mismo monto se afecta la cuenta del plan contable. Es decir si tenia 200 USD ahora en lugar de tener 416 USD tengo 1 000 200 USD.
    """,
    'author':  'OpenERP Team de Localizacion Argentina',
    'images': [
    ],
    'depends': [
        'account_voucher'
    ],
    'data': [
        'wizard/check_action_view.xml',
        'wizard/view_check_reject.xml',
        'views/account_checkbook_view.xml',
        'views/account_view.xml',
        'views/account_voucher_view.xml',
        'views/account_check_view.xml',
        'workflow/account_check_workflow.xml',
        'workflow/workflow_checkbook.xml',
        'security/ir.model.access.csv',
        'security/account_check_security.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
