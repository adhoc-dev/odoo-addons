# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp.osv import osv


class product_force_create_variant(osv.osv_memory):
    _name = "product.force_create_variant"
    _description = "product.force_create_variant"

    def create_variants(self, cr, uid, ids, context=None):
        product_template_ids = context.get('active_ids', [])
        return self.pool['product.template'].create_variant_ids(
            cr, uid, product_template_ids, context=context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
