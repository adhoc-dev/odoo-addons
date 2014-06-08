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
#    This program is distributed in the hope that it wil    l be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv, fields
from openerp import tools
from openerp.tools.translate import _

class product_supplierinfo(osv.osv):
    _inherit = 'product.supplierinfo'

    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if not ids:
            return []
        reads = self.read(cr, uid, ids, ['name','product_id'], context=context)
        res = []
        for record in reads:
            name = record['name'][1]
            if record['product_id']:
                name = record['product_id'][1]+' - '+name
            res.append((record['id'], name))
        return res

    def _model_name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)

    _rec_name = 'complete_name'

    _columns={
        'complete_name': fields.function(_model_name_get_fnc, type="char", string='Name',),
    }

    _sql_constraints = [
        ('supplier_unique', 'unique (name,product_id,company_id)', 'The record must be unique for a product and partner on the same company!'),
    ] 


class pricelist_partnerinfo(osv.osv):
    _name = 'pricelist.partnerinfo'
    _inherit = 'pricelist.partnerinfo'
    _columns = {
        'partner_id' : fields.related('suppinfo_id', 'name', domain = [('supplier','=',True)], relation='res.partner', store=True, type='many2one', string='Supplier', readonly="1", help="Supplier of this product"),
        'product_uom': fields.related('suppinfo_id', 'product_id', 'uom_po_id', store=True, type='many2one', relation='product.uom', string="Supplier Unit of Measure", readonly="1", help="This comes from the product form."),
        'product_id' : fields.related('suppinfo_id', 'product_id', relation='product.product', store=True, type='many2one', string='Product', readonly="1",),
#campos agregados pero luego eliminados
        # 'product_name': fields.related('suppinfo_id', 'product_name', string='Supplier Product Name', type='char', size=128, help="This supplier's product name will be used when printing a request for quotation. Keep empty to use the internal one."),
        # 'product_code': fields.related('suppinfo_id', 'product_code', string='Supplier Product Code', type='char', size=64, help="This supplier's product code will be used when printing a request for quotation. Keep empty to use the internal one."),
        # 'min_qty': fields.related('suppinfo_id', 'min_qty', string='Minimal Quantity', required=True, type='float', help="The minimal quantity to purchase to this supplier, expressed in the supplier Product Unit of Measure if not empty, in the default unit of measure of the product otherwise."),
        # este no se para que era usado
        # 'qty': fields.function(_calc_qty, store=True, type='float', string='Quantity', multi="qty", help="This is a quantity which is converted into Default Unit of Measure."),
        # 'delay': fields.related('suppinfo_id', 'delay', string='Delivery Lead Time', required=True, type='integer', help="Lead time in days between the confirmation of the purchase order and the reception of the products in your warehouse. Used by the scheduler for automatic computation of the purchase order planning."),
        # 'company_id' : fields.related('suppinfo_id', 'company_id', relation='res.company', type='many2one', string='Company',),
    }

    _sql_constraints = [
        ('pricelist_unique', 'unique (suppinfo_id,min_quantity)', 'The record must be unique for Quantity, Supplier and Product!'),
    ] 


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
