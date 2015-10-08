# -*- coding: utf-8 -*-
from openerp import models, api


class account_voucher(models.Model):
    _inherit = 'account.voucher'

    @api.multi
    def receipt_print(self):
        '''This function prints the picking list'''
        self.ensure_one()
        report_obj = self.env['ir.actions.report.xml']
        report_name = report_obj.get_report_name('account.voucher', self.ids)
        return self.env['report'].get_action(self, report_name)

    def receipt_send_rfq(self, cr, uid, ids, context=None):
        '''
        This function opens a window to compose an email, with the edi receipt template message loaded by default
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        ir_model_data = self.pool.get('ir.model.data')
        try:
            template_id = ir_model_data.get_object_reference(cr, uid, 'report_extended_voucher', 'email_template_edi_receipt')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference(cr, uid, 'mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False 
        ctx = dict()
        ctx.update({
            'default_model': 'account.voucher',
            'default_res_id': ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
