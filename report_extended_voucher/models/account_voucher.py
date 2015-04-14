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
