# -*- encoding: utf-8 -*-
{
    "name": "Add Vat option on partner_views_fields",
    "version": "8.0.1.0.0",
    "author": "ADHOC SA",
    "category": "",
    "description" : """
Add Fields on Partners Views
============================
    """,
    "website": "www.adhoc.com.ar",
    'license': 'AGPL-3',
    "depends": [
        "partner_views_fields",
        "base_vat",
                ],
    "demo": [
    ],
    "data": [
        'security/partner_person_security.xml',
        'res_partner_view.xml',
        'res_config_view.xml',
    ],
    "installable": True,
    "active": False,
    'auto_install': True,
}
