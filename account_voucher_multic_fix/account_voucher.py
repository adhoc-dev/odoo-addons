# -*- coding: utf-8 -*-
from openerp import models


class account_voucher(models.Model):

    _inherit = "account.voucher"

    def on_change_company(
            self, cr, uid, ids, date, currency_id, payment_rate_currency_id,
            amount, company_id, context=None):
        ''' We replace the original one by this function so that journal_id
        value and domain is updated
        when company_id is change. We also call to onchange_date in order to
        update the selected period'''
        # Run onchange_date to update period and other values
        result = self.onchange_date(
            cr, uid, ids, date, currency_id, payment_rate_currency_id, amount,
            company_id, context=context)
        if 'domain' not in result:
            result['domain'] = {}
        if 'value' not in result:
            result['value'] = {}

        journal_id = False
        journal_ids = []
        if company_id:
            domain = [
                ('company_id', '=', company_id),
                ('type', 'in', ('cash', 'bank'))]
            # Esto seria si esta instalado el modulo de direction
            if self.pool['account.journal'].fields_get(cr, uid, ['direction']):
                if context.get('type', False) == 'payment':
                    domain.append(('direction', 'in', [False, 'out']))
                elif context.get('type', False) == 'receipt':
                    domain.append(('direction', 'in', [False, 'in']))
            journal_ids = self.pool['account.journal'].search(
                cr, uid, domain, context=context)
            if journal_ids:
                journal_id = journal_ids[0]
        journal_domain = [('id', 'in', journal_ids)]
        result['domain']['journal_id'] = journal_domain
        result['value']['journal_id'] = journal_id
        return result

    def recompute_voucher_lines(
            self, cr, uid, ids, partner_id, journal_id, price, currency_id,
            ttype, date, context=None):
        '''Modification of this method so that only the moves of selected
        journal company are considered'''

        if not context:
            context = {}
        move_line_pool = self.pool.get('account.move.line')
        journal_pool = self.pool.get('account.journal')
        journal = journal_pool.browse(cr, uid, journal_id, context=context)
        account_type = None
        if context.get('account_id'):
            account_type = self.pool['account.account'].browse(
                cr, uid, context['account_id'], context=context).type
        if ttype == 'payment':
            if not account_type:
                account_type = 'payable'
        else:
            if not account_type:
                account_type = 'receivable'
        move_line_ids = move_line_pool.search(cr, uid, [
            ('state', '=', 'valid'),
            ('company_id', '=', journal.company_id.id),
            ('account_id.type', '=', account_type),
            ('reconcile_id', '=', False),
            ('partner_id', '=', partner_id)], context=context)
        if move_line_ids:
            context['move_line_ids'] = move_line_ids
        else:
            return {
                'value': {
                    'line_dr_ids': [], 'line_cr_ids': [], 'pre_line': False},
            }
        return super(account_voucher, self).recompute_voucher_lines(
            cr, uid, ids, partner_id, journal_id, price, currency_id, ttype,
            date, context=context)
