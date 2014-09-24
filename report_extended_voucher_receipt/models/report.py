# -*- coding: utf-8 -*-
from openerp import models, fields


class ir_actions_report(models.Model):
    _inherit = 'ir.actions.report.xml'

    receiptbook_ids = fields.Many2many(
        'account.voucher.receiptbook', 'report_configuration_receiptbook_rel',
        'report_configuration_id', 'receiptbook_id', 'ReceiptBooks')
    receipt_type = fields.Selection(
        [('payment', 'Payment'), ('receipt', 'Receipt')], 'Receipt Type', )

    def get_domains(self, cr, model, record, context=None):
        domains = super(ir_actions_report, self).get_domains(
            cr, model, record, context=context)
        if model == 'account.voucher.receipt':
            # Search for especific report
            domains.append([('receipt_type', '=', record.type),
                            ('receiptbook_ids', '=', record.receiptbook_id.id)])
            # Search without type
            domains.append(
                [('receipt_type', '=', False), ('receiptbook_ids', '=', record.receiptbook_id.id)])
            # Search without receiptbooks and with type
            domains.append(
                [('receipt_type', '=', record.type), ('receiptbook_ids', '=', False)])
            # Search without receiptbooks and without type
            domains.append(
                [('receipt_type', '=', False), ('receiptbook_ids', '=', False)])
        return domains
