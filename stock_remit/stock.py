# -*- coding: utf-8 -*-
from openerp import fields, models, _
from openerp.osv import osv


class stock_picking_type(models.Model):
    _inherit = "stock.picking.type"

    remit_sequence_id = fields.Many2one('ir.sequence', 'Remit Sequence')


class stock_picking(models.Model):
    _inherit = 'stock.picking'

    remit_number = fields.Char('Remit Number', copy=False)

    _sql_constraints = [
        ('remit_number_uniq', 'unique(remit_number, company_id)',
            _('The field "Remit Number" must be unique per company.'))]

    def do_print_picking(self, cr, uid, ids, context=None):
        '''This function prints the picking list'''
        stock_report_type = context.get('stock_report_type', False)
        from_wizard = context.get('from_wizard', False)
        if not from_wizard and stock_report_type == 'remit':
            mod_obj = self.pool['ir.model.data']
            act_obj = self.pool['ir.actions.act_window']
            action = mod_obj.get_object_reference(
                cr, uid, 'stock_remit', 'action_stock_print_remit')
            action_id = action and action[1] or False
            action = act_obj.read(cr, uid, [action_id], context=context)[0]
            return action
        else:
            return super(stock_picking, self).do_print_picking(
                cr, uid, ids, context=context)

    def set_remit_number(self, cr, uid, ids, context=None):
        if not isinstance(ids, list):
            ids = [ids]

        sequence_obj = self.pool.get('ir.sequence')
        picking_obj = self.pool.get('stock.picking')

        for picking in self.browse(cr, uid, ids, context=context):
            if not picking.picking_type_id.remit_sequence_id:
                title = _('No sequence defined')
                message = _(
                    'There is sequence defined for the current Picking Type.')
                raise osv.except_osv(title, message)

            remit_sequence_id = picking.picking_type_id.remit_sequence_id.id
            next_seq_num = sequence_obj.next_by_id(
                cr, uid, remit_sequence_id, context=context)
            picking_obj.write(
                cr, uid, picking.id,
                {'remit_number': next_seq_num}, context=context)
