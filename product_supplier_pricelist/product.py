# -*- coding: utf-8 -*-
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
        reads = self.read(
            cr, uid, ids, ['name', 'product_id'], context=context)
        res = []
        for record in reads:
            name = record['name'][1]
            if record['product_id']:
                name = record['product_id'][1] + ' - ' + name
            res.append((record['id'], name))
        return res

    def _model_name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)

    _rec_name = 'complete_name'

    _columns = {
        'complete_name': fields.function(_model_name_get_fnc, type="char", string='Name',),
    }

    _sql_constraints = [
        ('supplier_unique', 'unique (name, product_id, company_id)',
         'The record must be unique for a product and partner on the same company!'),
    ]


class pricelist_partnerinfo(osv.osv):
    _inherit = 'pricelist.partnerinfo'
    _columns = {
        'partner_id': fields.related('suppinfo_id', 'name', domain=[('supplier', '=', True)], relation='res.partner', store=True, type='many2one', string='Supplier', readonly="1", help="Supplier of this product"),
        'product_uom': fields.related('suppinfo_id', 'product_id', 'uom_po_id', store=True, type='many2one', relation='product.uom', string="Supplier Unit of Measure", readonly="1", help="This comes from the product form."),
        'product_id': fields.related('suppinfo_id', 'product_id', relation='product.product', store=True, type='many2one', string='Product', readonly="1",),
    }

    _sql_constraints = [
        ('pricelist_unique', 'unique (suppinfo_id,min_quantity)',
         'The record must be unique for Quantity, Supplier and Product!'),
    ]


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
