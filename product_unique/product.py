# -*- coding: utf-8 -*-
##############################################################################
#
#    Ingenieria ADHOC - ADHOC SA
#    https://launchpad.net/~ingenieria-adhoc
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

from openerp.osv import osv, fields

def _check_unique_company_and_default_code(self, cr, uid, ids, context=None):
    for product in self.browse(cr, uid, ids, context=context):
		if product.active and product.default_code and product.company_id:
			filters = [('company_id', '=', product.company_id.id), ('default_code', '=', product.default_code), ('active', '=', True)]
			prod_ids = self.search(cr, uid, filters, context=context)
			if len(prod_ids) > 1:
				return False
		return True

def _check_unique_company_and_ean13(self, cr, uid, ids, context=None):
    for product in self.browse(cr, uid, ids, context=context):
		if product.active and product.ean13 and product.company_id:
			filters = [('company_id', '=', product.company_id.id), ('ean13', '=', product.ean13), ('active', '=', True)]
			prod_ids = self.search(cr, uid, filters, context=context)
			if len(prod_ids) > 1:
				return False
		return True

class product_product(osv.osv):
	_name = "product.product"
	_inherit = "product.product"

	_columns = {
		'company_id': fields.related('product_tmpl_id', 'company_id', type='many2one', relation='res.company', string='Company', store=True, select=True),
	}

	_constraints = [
		(_check_unique_company_and_default_code, ('There can not be two active products with the same Reference ode in the same company.'), ['company_id', 'default_code', 'active']),
		(_check_unique_company_and_ean13, ('There can not be two active products with the same EAN code in the same company'), ['company_id', 'ean13', 'active'])	
	]

product_product()           