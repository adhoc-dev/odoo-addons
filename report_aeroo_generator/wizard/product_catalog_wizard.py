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

class product_catalog_wizard(osv.osv_memory):
    _name = 'report_aeroo_generator.product_catalog_wizard'
    _description = 'Wizard to generate the Product Catalog Report with Aeroo'

    _columns = {
        'category_ids': fields.many2many('product.category', 'product_catalog_aeroo_report_categories','wizard_id', 'category_id', _('Product Categories'), required=True),
        'pricelist_id': fields.many2one('product.pricelist', _('Pricelist'), required=True)
    }
    
    def generate_report(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids)[0]
        
        categories = wizard.category_ids
        if not categories:
            return {'type': 'ir.actions.act_window_close'}
        if not isinstance(categories, list):
            categories = [categories]
        context['category_ids'] = map(lambda cat: cat.id, categories)
        
        pricelist_id = wizard.pricelist_id.id
        if isinstance(pricelist_id, list):
            pricelist_id = pricelist_id[0]
        context['pricelist_id'] = pricelist_id
        result = {'type' : 'ir.actions.report.xml',
                  'context' : context,
                  'report_name': 'report_product_catalog',}
        return result
        
product_catalog_wizard()

