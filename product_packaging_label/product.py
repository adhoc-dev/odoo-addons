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

from osv import osv
from osv import fields
from tools.translate import _

class product_packaging_label(osv.osv):
    _name = 'product.packaging.label'
    _description = 'Product Packaging Labels'
    _rec_name = 'description'
        
    _columns = {
        # 'name': fields.char('Name', required=True),
        # 'quantity': fields.integer('Quantity', required=True),
        'description': fields.text('Description', required=True),
        'product_id': fields.many2one('product.template', 'Product Template', required=True),
    }

class product_template(osv.osv):
    _inherit = 'product.template'
    # _inherit = 'product.template'

    _columns = {
        'packaging_label_ids': fields.one2many('product.packaging.label', 'product_id','Packaging Labels', required=True),
    }    








