# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
    'name': 'Price Security for Product Visible Discount',
    'version': '1.0',
    'category': 'Hidden',
    'description': """
    In prescense of product_visible_discount and price_security, extend the discount
    that the user can do on a sale order or invoice to include the one done by the
    pricelist.
    """,
    'author': 'ADHOC Sistemas',
    'website': 'http://www.adhocsistemas.com.ar/',
    'depends': ['product_visible_discount', 'price_security'],
    'init_xml': [],
    'update_xml': [],
    'demo_xml': [],
    'test':[],
    'installable': True,
    'auto_install': True,
}
