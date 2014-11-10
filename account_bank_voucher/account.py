# -*- coding: utf-8 -*-
from openerp import models, fields


class account_bank_statement_line(models.Model):
    _inherit = 'account.bank.statement.line'
    voucher_id = fields.Many2one('account.voucher', 'Voucher')


class account_voucher(models.Model):
    _inherit = 'account.voucher'

    # is_bank_voucher = fields.boolean('Bank Voucher')
    bank_statement_line_ids = fields.One2many(
        'account.bank.statement.line', 'voucher_id', string="Statement Lines")

    # def filter_bank_voucher_ids_by_key(self, cr, uid, ids, key, context=None):
    #     if context is None:
    #         context = {}
    #     voucher_ids = []
    #     if context.get(key, False):
    #         for v in self.read(cr, uid, ids, ['is_bank_voucher'], context=context):
    #             if not v['is_bank_voucher']:
    #                 voucher_ids.append(v['id'])
    #     else:
    #         voucher_ids = ids
    #     return voucher_ids

    # def unlink(self, cr, uid, ids, context=None):
    #     return super(account_voucher, self).unlink(cr, uid,
    #                                                self.filter_bank_voucher_ids_by_key(
    #                                                    cr, uid, ids, 'account_bank_voucher_unlink', context=context),
    #                                                context=context)

    # def cancel_voucher(self, cr, uid, ids, context=None):
    #     return super(account_voucher, self).cancel_voucher(cr, uid,
    #                                                        self.filter_bank_voucher_ids_by_key(
    #                                                            cr, uid, ids, 'account_bank_voucher_button_cancel', context=context),
    #                                                        context=context)


# class account_bank_statement(Models.model):
#     _inherit = 'account.bank.statement'

#     def button_cancel(self, cr, uid, ids, context=None):
#         if context is None:
#             context = {}
#         context['account_bank_voucher_button_cancel'] = True
#         return super(account_bank_statement, self).button_cancel(cr, uid, ids, context=context)


# class account_bank_statement_line(Models.model):
#     _inherit = 'account.bank.statement.line'

#     def unlink(self, cr, uid, ids, context=None):
#         if context is None:
#             context = {}
#         context['account_bank_voucher_unlink'] = True
#         return super(account_bank_statement_line, self).unlink(cr, uid, ids, context=context)
