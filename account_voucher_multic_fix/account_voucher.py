# -*- coding: utf-8 -*-
from openerp import models, api, fields


class account_voucher(models.Model):

    _inherit = "account.voucher"

    available_journal_ids = fields.Many2many(
        'account.journal',
        compute='_get_available_journals',
        string='Available Journals',
        )

    @api.one
    @api.depends('company_id')
    def _get_available_journals(self):
        self.available_journal_ids = self.env['account.journal']
        journal_ids = []
        if self.company_id:
            domain = [
                ('company_id', '=', self.company_id.id),
                ('type', 'in', ('cash', 'bank'))]
            # Esto seria si esta instalado el modulo de direction
            if self.env['account.journal'].fields_get(['direction']):
                if self._context.get('type', False) == 'payment':
                    domain.append(('direction', 'in', [False, 'out']))
                elif self._context.get('type', False) == 'receipt':
                    domain.append(('direction', 'in', [False, 'in']))
            journal_ids = self.env['account.journal'].search(domain)
        self.available_journal_ids = journal_ids

    @api.onchange('company_id')
    def on_change_company_new_api(self):
        """El onchange por defecto de account voucher esta presente en algunas
        vistas y otras no, por eso lo borramos de la que nos interesa y lo 
        hacemos con la nueva api. El onchange original no hacia mucho que
        digamos
        """
        self.journal_id = self.available_journal_ids and self.available_journal_ids[0].id or False
        # TODO antes era necesiaro cambiar el periodo pero parece que ahora no
        # por las dudas dejamos algo de codigo que deberia ayudar en tal caso
        # result = self.onchange_date(
        #     cr, uid, ids, date, currency_id, payment_rate_currency_id, amount,
        #     company_id, context=context)
        # y de result tenemos que tomar period

    def recompute_voucher_lines(
            self, cr, uid, ids, partner_id, journal_id, price, currency_id,
            ttype, date, context=None):
        '''Modification of this method so that only the moves of selected
        journal company are considered.
        We select the move lines and send them in the context'''
        # TODO cambiar a nueva api

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
