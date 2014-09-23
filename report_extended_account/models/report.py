# -*- coding: utf-8 -*-
from openerp import models, fields


class ir_actions_report(models.Model):
    _inherit = 'ir.actions.report.xml'

    account_invoice_state = fields.Selection(
        [('proforma', 'Pro-forma'), ('approved_invoice', 'Aproved Invoice')],
        'Invoice State', required=False)
    account_invoice_journal_ids = fields.Many2many(
        'account.journal', 'report_account_journal_rel', 'report_id',
        'journal_id', 'Journals',
        domain=[('type', 'in', ['sale', 'sale_refund'])])
    account_invoice_split_invoice = fields.Boolean(
        'Split Inovice',
        help='If true, when validating the invoice, if it contains more than the specified number of lines, new invoices will be generated.')
    account_invoice_lines_to_split = fields.Integer(
        'Lines to split')

    def get_domains(self, cr, model, record, context=None):
        domains = super(ir_actions_report, self).get_domains(
            cr, model, record, context=context)
        if model == 'account.invoice':
            account_invoice_state = False

            # We user ignore_state to get the report to split invoice before
            # the invoice is validated
            ignore_state = context.get('ignore_state', False)
            if ignore_state:
                account_invoice_state = ['approved_invoice', 'proforma', False]
            elif record.state in ['proforma', 'proforma2']:
                account_invoice_state = ['proforma']
            elif record.state in ['open', 'paid', 'sale']:
                account_invoice_state = ['approved_invoice']
            # Search for especific report
            domains.append([('account_invoice_state', 'in', account_invoice_state),
                            ('account_invoice_journal_ids', '=', record.journal_id.id)])
            # Search without state
            domains.append(
                [('account_invoice_state', 'in', account_invoice_state), ('account_invoice_journal_ids', '=', False)])
            # Search without journal and state
            domains.append([('account_invoice_state', '=', False),
                            ('account_invoice_journal_ids', '=', record.journal_id.id)])
            # Search without journal and without state
            domains.append(
                [('account_invoice_state', '=', False), ('account_invoice_journal_ids', '=', False)])
        return domains
