# -*- coding: utf-8 -*-


{
    'name': 'Partners Persons Management',
    'version': '1.0',
    'category': 'Tools',
    'sequence': 14,
    'summary': '',
    'description': """
Partners Persons Management
===========================

Openerp consider a person those partners that have not "is_company" as true, now, those partners can have:
----------------------------------------------------------------------------------------------------------

* First Name and Last Name 
* Birthdate
* Sex
* Mother and Father
* Childs
* Age (functional field)
* Nationality
* Husband/Wife
* National Identity
* Passport
* Marital Status

It also adds a configuration menu for choosing which fields do you wanna see.
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'base',
    ],
    'data': [
        'res_partner_view.xml',
        'res_config_view.xml',
        'security/partner_person_security.xml',
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