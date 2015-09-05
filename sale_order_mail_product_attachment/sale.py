# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models


class sale_order_line(models.Model):
    _inherit = "sale.order.line"

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
        res = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty,
            uom, qty_uos, uos, name, partner_id,
            lang, update_tax, date_order, packaging, fiscal_position, flag, context)
        partner_obj = self.pool.get('res.partner')
        lang = partner_obj.browse(cr, uid, partner_id).lang
        context_partner = {'lang': lang, 'partner_id': partner_id}
        product_obj = self.pool.get('product.product')
        attachment_obj = self.pool['ir.attachment']
        if product:
            product_obj = product_obj.browse(cr, uid, product, context=context_partner)        
            if not flag:
                attachment_ids = attachment_obj.search(cr, uid, [('res_model','=','product.product'),('res_id','=',product)], context=context)
                if attachment_ids:
                    attachemnt_desc = ', '.join([at.name for at in attachment_obj.browse(cr, uid, attachment_ids, context=context)])
                    res['value']['name'] += '\n' + ('Ver adjuntos: ') + attachemnt_desc           
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
