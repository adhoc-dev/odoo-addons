# -*- coding: utf-8 -*-
from lxml import etree
from openerp.osv import fields, osv


class account_voucher_populate_statement(osv.osv_memory):
    _name = "account.voucher.populate.statement"
    _description = "Account Voucher Populate Statement"
    _columns = {
        'lines': fields.many2many('account.voucher', 'account_voucher_line_rel_', 'voucher_id', 'line_id', 'Vouchers')
    }

    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        if context is None:
            context = {}
        line_obj = self.pool.get('account.voucher')
        res = super(account_voucher_populate_statement, self).fields_view_get(
            cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=False)
        if view_type != 'form' or not context.get('active_id', False):
            return res
        statement = self.pool.get('account.bank.statement').browse(
            cr, uid, context.get('active_id'), context=context)
        account_ids = [statement.journal_id.default_credit_account_id.id,
                       statement.journal_id.default_debit_account_id.id]
        journal_ids = self.pool.get('account.journal').search(cr, uid, [
            '|', ('default_credit_account_id', 'in', account_ids),
            ('default_debit_account_id', 'in', account_ids)], context=context)
        line_ids = line_obj.search(cr, uid, [
            ('type', 'not in', ['sale', 'purchase']),
            ('bank_statement_line_ids', '=', False),
            ('state', '=', 'posted'),
            '|', ('journal_id', 'in', journal_ids),
            ('line_ids.account_id', 'in', account_ids)], context=context)
        domain = '[("id", "in", ' + str(line_ids) + ')]'
        doc = etree.XML(res['arch'])
        nodes = doc.xpath("//field[@name='lines']")
        for node in nodes:
            node.set('domain', domain)
        res['arch'] = etree.tostring(doc)
        return res

    def get_statement_line_new(self, cr, uid, voucher, statement, context=None):
        # Override thi method to modifiy the new statement line to create
        ctx = context.copy()
        ctx['date'] = voucher.date
        amount = self.pool.get('res.currency').compute(cr, uid, voucher.currency_id.id,
                                                       statement.currency.id, voucher.amount, context=ctx)

        sign = voucher.type == 'payment' and -1.0 or 1.0
        type = voucher.type == 'payment' and 'supplier' or 'customer'
        account_id = voucher.type == 'payment' and voucher.partner_id.property_account_payable.id or voucher.partner_id.property_account_receivable.id
        return {
            'name': voucher.reference or voucher.number or '?',
            'amount': sign * amount,
            'type': type,
            'partner_id': voucher.partner_id.id,
            'account_id': account_id,
            'statement_id': statement.id,
            'ref': voucher.name,
            'voucher_id': voucher.id,
        }

    def populate_statement(self, cr, uid, ids, context=None):
        statement_obj = self.pool.get('account.bank.statement')
        statement_line_obj = self.pool.get('account.bank.statement.line')
        voucher_obj = self.pool.get('account.voucher')

        if context is None:
            context = {}
        data = self.read(cr, uid, ids, [], context=context)[0]
        voucher_ids = data['lines']
        if not voucher_ids:
            return {'type': 'ir.actions.act_window_close'}
        statement = statement_obj.browse(
            cr, uid, context['active_id'], context=context)
        for voucher in voucher_obj.browse(cr, uid, voucher_ids, context=context):
            statement_line_obj.create(cr, uid,
                                      self.get_statement_line_new(cr, uid, voucher, statement, context=context), context=context)
        voucher_obj.write(
            cr, uid, voucher_ids, {'is_bank_voucher': True}, context=context)
        return {'type': 'ir.actions.act_window_close'}

account_voucher_populate_statement()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
