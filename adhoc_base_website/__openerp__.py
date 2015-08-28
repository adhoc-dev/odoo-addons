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
    'name': 'ADHOC Modules Configuration - Website',
    'version': '8.0.1.1.0',
    'category': 'ADHOC Modules',
    'summary': 'extra, addons, modules',
    'description': """
ADHOC Modules Configuration - Website
===============================================================================
Here, you can configure the whole business suite based on your requirements. You'll be provided different configuration options in the Settings where by only selecting some booleans you will be able to install several modules and apply access rights in just one go.
Repositories required:
---------------------
* https://github.com/OCA/website/tree/8.0/website_logo
* https://github.com/OCA/website/tree/8.0/website_sale_collapse_categories
* https://github.com/OCA/website/tree/8.0/website_sale_vat_required
""",

    'author':  'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'images': [
    ],
    'depends': [
        'adhoc_base_setup',
        'website'
    ],
    'data': [
        'res_config_view.xml',
    ],
    'demo': [],
    'test': [
    ],
    'installable': True,
    'auto_install': True,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
