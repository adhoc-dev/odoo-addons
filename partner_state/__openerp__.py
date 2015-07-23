# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015  ADHOC SA  (http://www.adhoc.com.ar)
#    All Rights Reserved.
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
    'author': 'ADHOC SA',
    'website': 'www.adhoc.com.ar',
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
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
