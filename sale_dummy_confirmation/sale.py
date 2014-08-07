# -*- coding: utf-8 -*-
from openerp import api, fields, models, _

class sale_order(models.Model):
    _inherit = 'sale.order'

    dummy_confirmation = fields.Boolean('Dummy Confirmation', help="If true, this sale order has been dummy confirmed and can go back to draft.")
        
    def action_button_confirm(self, cr, uid, ids, context=None):
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        so = self.browse(cr, uid, ids[0], context=context)
        if so.company_id.sale_order_dummy_confirm:
            so.write({'state':'done','dummy_confirmation':True})
            # redisplay the record as a sales order
            view_ref = self.pool.get('ir.model.data').get_object_reference(
                cr, uid, 'sale', 'view_order_form')
            view_id = view_ref and view_ref[1] or False
            return {
                'type': 'ir.actions.act_window',
                'name': _('Sales Order'),
                'res_model': 'sale.order',
                'res_id': ids[0],
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': view_id,
                'target': 'current',
                'nodestroy': True,
            }
        else:        
            res = super(sale_order, self).action_button_confirm(cr, uid, ids, context=context)
