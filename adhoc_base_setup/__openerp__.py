# -*- coding: utf-8 -*-
{
    'name': 'ADHOC Modules Configuration',
    'version': '1.0',
    'category': 'ADHOC Modules',
    'summary': 'extra, addons, modules',
    'description': """
ADHOC Modules Configuration
===============================================================================
Here, you can configure the whole business suite based on your requirements. You'll be provided different configuration options in the Settings where by only selecting some booleans you will be able to install several modules and apply access rights in just one go.
Repositories required:
---------------------
* https://github.com/ingadhoc/odoo-addons
* https://github.com/ingadhoc/odoo-web
* https://github.com/akretion/odoo-usability
* https://github.com/OCA/account-invoicing
* https://github.com/OCA/knowledge
* https://github.com/OCA/server-tools
* https://github.com/OCA/account-financial-reporting
* https://github.com/OCA/account-financial-tools
* https://github.com/OCA/reporting-engine
* https://github.com/OCA/purchase-workflow
* https://github.com/aeroo/aeroo_reports
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
        'demo/company_demo.xml',
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': True,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
