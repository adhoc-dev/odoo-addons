# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api


class purchase_order(models.Model):
    _inherit = 'purchase.order'

    internal_notes = fields.Text('Internal Notes')

    def print_quotation(self, cr, uid, ids, context=None):
        '''
        This function prints the request for quotation and mark it as sent,
        so that we can see more easily the next step of the workflow
        '''
        assert len(
            ids) == 1, 'This option should only be used for a single id at a time'
        self.signal_workflow(cr, uid, ids, 'send_rfq')

        report_obj = self.pool.get('ir.actions.report.xml')
        report_name = report_obj.get_report_name(
            cr, uid, 'purchase.order', ids, context=context)
        return self.pool['report'].get_action(
            cr, uid, ids, report_name, context=context)

    @api.model
    def _prepare_invoice(self, order, line_ids):
        invoice_vals = super(
            purchase_order, self)._prepare_invoice(order, line_ids)
        invoice_vals.update({
            'comment': order.internal_notes})
        return invoice_vals

    @api.model
    def action_picking_create(self):
        picking_id = super(purchase_order, self).action_picking_create()
        picking = self.env['stock.picking'].browse(picking_id)
        picking.write({'note': self.internal_notes})
        return picking_id
