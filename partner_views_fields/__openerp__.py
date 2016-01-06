# -*- encoding: utf-8 -*-
{
    "name": "Add Fields on Partners Views",
    "version": "8.0.0.1.1",
    "author": "ADHOC SA",
    "category": "",
    "description": """
Add Fields on Partners Views
============================
    """,
    "website": "www.adhoc.com.ar",
    'license': 'AGPL-3',
    "depends": [
        "base_setup",
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
}
