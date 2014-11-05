# -*- coding: utf-8 -*-
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
    'auto_install': True,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: