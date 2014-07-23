# -*- coding: utf-8 -*-
##############################################################################
#
#    Sistemas ADHOC - ADHOC SA
#    https://launchpad.net/~sistemas-adhoc
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
    'name': 'Fetchmail ADHOC',
    'version': '1.0',
    'category': 'Tools',
    'sequence': 14,
    'summary': '',
    'description': """
Fetchmail ADHOC
===============
Prerequisitos:
--------------
* Configuración de postfix (unica vez):
    Se debe configurar postfix de determinada manera, se puede seguir el siguiente tutorial:
    https://docs.google.com/a/ingadhoc.com/document/d/1Xpwe3n_TQEBc5jjbZNR5OJaXcPBQKPQLLuF4G38GHY4/edit

* Cambiar permisos sobre archivos (unica vez):
    sudo chown root.openerp /etc/postfix/virtual_aliases
    sudo chmod g+w /etc/postfix/virtual_aliases
    sudo chown root.openerp /etc/aliases
    sudo chmod g+w /etc/aliases
    sudo chown root.openerp /etc/postfix/virtual_aliases.db
    sudo chmod g+w /etc/postfix/virtual_aliases.db
    sudo chown root.openerp /etc/aliases.db
    sudo chmod g+w /etc/aliases.db
* Habilitar correr comando con sudo sin clave (unica vez):
    sudo visudo
    agregar estas lineas:
        # Permite reiniciar el servicio postfix a los usuarios del gurpo openerp
        %openerp ALL=(ALL:ALL) NOPASSWD: /etc/init.d/postfix restart        
    
* Cada vez que se agregue un nuevo dominio:
    Para cada nuevo dominio que queremos que postfix acepte se debe agregar una expresion regular en /etc/postfix/virtual_domain_regex
    """,
    'author':  'Sistemas ADHOC',
    'website': 'www.sistemasadhoc.com.ar',
    'images': [
    ],
    'depends': [
        'fetchmail',
    ],
    'data': [
        'res_config_view.xml',
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