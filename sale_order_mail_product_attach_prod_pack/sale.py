# -*- encoding: latin-1 -*-
from openerp import models


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    def create(self, cr, uid, vals, context=None):
        # if pack_parent_line_id the it is a child product of a pack
        product_id = vals.get('product_id', False)
        if vals.get('pack_parent_line_id', False) and product_id:
            attachment_obj = self.pool['ir.attachment']
            attachment_ids = attachment_obj.search(
                cr, uid,
                [('res_model', '=', 'product.product'),
                    ('res_id', '=', product_id)], context=context)
            if attachment_ids:
                attachemnt_desc = ', '.join(
                    [at.name for at in attachment_obj.browse(
                        cr, uid, attachment_ids, context=context)])
                vals['name'] += '\n' + ('Ver adjuntos: ') + attachemnt_desc
        return super(sale_order_line, self).create(
            cr, uid, vals, context=context)
