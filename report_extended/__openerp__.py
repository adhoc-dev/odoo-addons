# -*- coding: utf-8 -*-
{
    'name': 'Report Configurator',
    'version': '1.0',
    'category': 'Reporting Subsystem',
    'sequence': 14,
    'summary': '',
    'description': """
Report Configurator
===================
This module allows users to define reports of Aeroo for different
objects such as invoice or sale order.
It creates the menu to the configuration objects in:
    Configuration / Personalization / Aeroo Reports / Report Configuration

The parser proved a serie of fields an functions to use in the odt:
    
    o report_configuration: The associated report configuration object.
    o company: The company object.
    o logo: If not False it contains the logo of the company.
    o use_background_image: Boolean indicating if the background image should
      be used or not.
    o background_image: The background image to be used.
    o format_vat: Function that takes a string an format is as a vat.
    o address_from_partner: Return the default address from a partner object,
      or False.
    o minus: Given 2 values x1 and x2 returns x1 - x2.
    o number_to_string: Takes a string of a quantity and returns the textual
      representation of the quantity.
    o net_price: Takes a gross quantity and a discount and return the gross
      applying the discount.
    """,
    'author':  'Sistemas ADHOC',
    'website': 'www.sistemasadhoc.com.ar',
    'images': [
    ],
    'depends': [
        'report',
    ],
    'data': [
        'views/company_view.xml',
        'views/report_view.xml',
        'security/security.xml',
        'security/ir.model.access.csv', #TODO borrar este parche de reglas, es por un error que me estaba dando al querer imprimir ocn users distintos de admin
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