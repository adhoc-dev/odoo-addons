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
    'name': 'ADHOC Modules Configuration',
    'version': '1.0',
    'category': 'ADHOC Modules',
    'sequence': 14,
    'summary': 'extra, addons, modules',
    'description': """
ADHOC Modules Configuration
===============================================================================
Here, you can configure the whole business suite based on your requirements. You'll be provided different configuration options in the Settings where by only selecting some booleans you will be able to install several modules and apply access rights in just one go.
Repositories required:
---------------------
* lp:server-env-tools (web_export_view da error por ahora)
* lp:account-financial-report
* lp:account-financial-tools
* lp:openerp-reporting-engines
* lp:web-addons
* lp:~ingenieria-adhoc/openerp-adhoc-project/trunk
* lp:~ingenieria-adhoc/openerp-adhoc-sale-purchase/trunk
* lp:~ingenieria-adhoc/openerp-adhoc-product/trunk
* lp:~ingenieria-adhoc/openerp-adhoc-misc/trunk
* lp:~ingenieria-adhoc/openerp-adhoc-account/trunk
* lp:~ingenieria-adhoc/openerp-adhoc-reports/trunk
* lp:~ingenieria-adhoc/openerp-adhoc-documentation/trunk
* lp:~ingenieria-adhoc/openerp-adhoc-stock/trunk

Features
+++++++++++++++
Product Features
--------------------
TODO


Warehouse Features
------------------------
TODO

Sales Features
--------------------
TODO

* TODO1
* TODO2
* TODO3

Purchase Features
-------------------------
TODO

* TODO1
* TODO2

Finance Features
------------------
TODO

Extra Tools
-------------
TODO

* TODO1
* TODO2
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'base_setup'
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
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: