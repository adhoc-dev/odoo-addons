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
    'name': 'Stock Move Change Location Control',
    'version': '1.0',
    'description': """
    If the location of a stock move is changed when it is the state Ready to Process,
    then the state of that move is changed to Waiting Availability.
    """,
    'category': 'Warehouse Management',
    'author': 'Sistemas ADHOC',
    'website': 'http://www.sistemasadhoc.com.ar/',
    'depends': ['stock'],
    'init_xml': [],
    'update_xml': [],
    'demo_xml': [],
    'test':[],
    'installable': True,
}

