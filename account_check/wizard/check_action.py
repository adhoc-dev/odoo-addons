# -*- coding: utf-8 -*-


from openerp.osv import osv, fields
from openerp.tools.translate import _
import time

class account_check_action(osv.osv_memory):
    _name = 'account.check.action'

    _columns = {
        'account_id': fields.many2one('account.account', 'Account', domain=[('type','in',['other','liquidity'])]),
        'date': fields.date('Debit Date',required=True),
        'action_type': fields.char('Action type passed on the context', required=True),
    }

    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d'),
    }

    def action_confirm(self, cr, uid, ids, context=None):
        check_obj = self.pool.get('account.check')
        move_line_obj = self.pool.get('account.move.line')
        wizard = self.browse(cr, uid, ids[0], context=context)
        period_id = self.pool.get('account.period').find(cr, uid, wizard.date)[0]
        if context is None:
            context = {}

        record_ids = context.get('active_ids', [])
        for check in check_obj.browse(cr, uid, record_ids, context=context):
            print 'check.type ', check.type 
            if check.type == 'third':
                if check.state != 'holding':
                    raise osv.except_osv(_('Check %s selected error' % (check.name)),
                        _('The selected checks must be in holding state.'))                    
            elif check.type == 'issue':
                if check.state != 'handed':
                    raise osv.except_osv(_('Check %s selected error' % (check.name)),
                        _('The selected checks must be in handed state.'))

            if wizard.action_type == 'deposit':
                # TODO: tal vez la cuenta de deposito del cheque deberia salir de la seleccion de un jorunal y el journal tambien.
                ref = _('Deposit Check Nr. ')
                check_move_field = 'deposit_account_move_id'
                journal = check.voucher_id.journal_id
                debit_account_id = wizard.account_id.id
                credit_account_id = check.voucher_id.journal_id.default_credit_account_id.id
                check_vals = {'deposit_account_id': debit_account_id}
                signal = 'holding_deposited'
            elif wizard.action_type == 'debit':
                ref = _('Debit Check Nr. ')
                check_move_field = 'debit_account_move_id'
                journal = check.checkbook_id.debit_journal_id
                debit_account_id = journal.default_debit_account_id.id
                credit_account_id = check.voucher_id.journal_id.default_credit_account_id.id
                check_vals = {}
                signal = 'handed_debited'

            name = self.pool.get('ir.sequence').next_by_id(cr, uid, journal.sequence_id.id, context=context)
            ref += check.name
            move_id = self.pool.get('account.move').create(cr, uid, {
                    'name': name,
                    'journal_id': journal.id,
                    'period_id': period_id,
                    'date': wizard.date,
                    'ref':  ref,
            })
            
            move_line_obj.create(cr, uid, {
                    'name': name,
                    'account_id': debit_account_id,
                    'move_id': move_id,
                    'debit': check.amount,
                    'ref': ref,
            })
            move_line_obj.create(cr, uid, {
                    'name': name,
                    'account_id': credit_account_id,
                    'move_id': move_id,
                    'credit': check.amount,
                    'ref': ref,
            })

            check_vals[check_move_field] = move_id
            check.write(check_vals)
            check.signal_workflow(signal)
        self.pool.get('account.move').write(cr, uid, [move_id], {'state': 'posted',})

        return {}