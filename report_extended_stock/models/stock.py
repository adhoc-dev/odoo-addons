# -*- coding: utf-8 -*-
from openerp import models, api


class stock_picking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def do_print_picking(self):
        '''This function prints the picking list'''
        assert len(self) == 1, 'This option should only be used for a single id at a time.'
        report_obj = self.env['ir.actions.report.xml']
        report_name = report_obj.with_context(
            stock_report_type='picking_list').get_report_name(
            'stock.picking', self.ids)
        return self.env['report'].get_action(self, report_name)

    @api.multi
    def do_print_voucher(self):
        '''This function prints the voucher'''
        assert len(self) == 1, 'This option should only be used for a single id at a time.'
        report_obj = self.env['ir.actions.report.xml']
        report_name = report_obj.with_context(
            stock_report_type='voucher').get_report_name(
            'stock.picking', self.ids)
        report = self.env['report'].get_action(self, report_name)
        if self._context.get('keep_wizard_open', False):
            report['type'] = 'ir.actions.report_dont_close_xml'
        return report


    # def receipt_send_rfq(self, cr, uid, ids, context=None):
    #     '''  Override to use a modified template that includes a portal signup link '''
    #     action_dict = super(stock_picking, self).receipt_send_rfq(cr, uid, ids, context=context)
    #     try:
    #         template_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'report_extended_stock', 'email_template_report_stock')[1]
    #         # assume context is still a dict, as prepared by super
    #         ctx = action_dict['context']
    #         ctx['default_template_id'] = template_id
    #         ctx['default_use_template'] = True
    #     except Exception:
    #         pass
    #     return action_dict

    # def receipt_send_rfq(self, cr, uid, ids, context=None):
    #     '''
    #     This function opens a window to compose an email, with the edi stock template message loaded by default
    #     '''
    #     assert len(ids) == 1, 'This option should only be used for a single id at a time.'
    #     ir_model_data = self.pool.get('ir.model.data')
    #     try:
    #         template_id = ir_model_data.get_object_reference(cr, uid, 'report_extended_stock', 'email_template_report_stock')[1]
    #     except ValueError:
    #         template_id = False
    #     try:
    #         compose_form_id = ir_model_data.get_object_reference(cr, uid, 'mail', 'email_compose_message_wizard_form')[1]
    #     except ValueError:
    #         compose_form_id = False 
    #     ctx = dict()
    #     ctx.update({
    #         'default_model': 'stock.picking',
    #         'default_res_id': ids[0],
    #         'default_use_template': bool(template_id),
    #         'default_template_id': template_id,
    #         'default_composition_mode': 'comment',
    #         'mark_so_as_sent': True
    #     })
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'mail.compose.message',
    #         'views': [(compose_form_id, 'form')],
    #         'view_id': compose_form_id,
    #         'target': 'new',
    #         'context': ctx,
    #     }
