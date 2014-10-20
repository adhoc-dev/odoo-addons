# -*- coding: utf-8 -*-
{'active': False,
    'author': 'Coop. Trab. Moldeo Interactive Ltda.',
    'category': 'Tools/Cryptography',
    'demo': [],
    'depends': [],
    'description': """
Cryptography Manager can generate key pairs and certificates to connect to
other services.""",
    'external_dependencies': {'python': ['M2Crypto']},
    'installable': True,
    'license': 'AGPL-3',
    'name': 'Cryptography Manager',
    'test': ['test/test_pairkey.yml', 'test/test_certificate.yml'],
    'data': [
        'crypto_menuitems.xml',
        'security/ir.model.access.csv',
        'wizard/generate_pairkey.xml',
        'wizard/generate_certificate.xml',
        'wizard/generate_certificate_request.xml',
        'pairkey_view.xml',
        'pairkey_workflow.xml',
        'certificate_view.xml',
        'certificate_workflow.xml'],
    'version': '0.8',
    'website': 'http://business.moldeo.coop'}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
