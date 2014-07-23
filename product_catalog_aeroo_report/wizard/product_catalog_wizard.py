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

from osv import fields, osv
from tools.translate import _

class product_catalog(osv.osv_memory):
    _name = 'product_catalog'
    _description = 'Wizard to generate the Product Catalog Report with Aeroo'


    _columns = {     
        'product_catalog_report_id':fields.many2one('product.product_catalog_report', 'Product Catalog', required=True),
    }

    _defaults = {
    }
    
    
    def generate_report(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids)[0]
        
        catalog = wizard.product_catalog_report_id
        if not catalog:
            return {'type': 'ir.actions.act_window_close'}

        return self.pool.get('product.product_catalog_report').generate_report(cr, uid, [catalog.id], context)
