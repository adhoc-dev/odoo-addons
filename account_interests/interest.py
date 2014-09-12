# -*- coding: utf-8 -*-
from openerp import fields, models, api, _


class account_account_interest(models.Model):
    _name = "account.account.interest"
    _description = 'Account Account Interest'

    account_id = fields.Many2one(
        'account.account',
        'Account',
        required=True,
        ondelete="cascade")
    interest_account_id = fields.Many2one(
        'account.account',
        'Interest Account',
        required=True,
        domain=[('type', '!=', 'view')])
    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        'Analytic account',
        domain=[('type', '!=', 'view')])
    interest_rate = fields.Float(
        'Interest',
        required=True,
        digits=(7, 4))
    date_from = fields.Date(
        'Date From',
        required=True)
    date_to = fields.Date('Date To')


class account_account(models.Model):
    _inherit = "account.account"

    account_account_interest_ids = fields.One2many(
        'account.account.interest',
        'account_id',
        'Interest Rates')

    def get_active_interest_data(self, cr, uid, ids, dt_from, dt_to, context=None):
        if context is None:
            context = {}
        interest_obj = self.pool.get('account.account.interest')
        res = {}

        for record_id in ids:
            interest_domain = [
                ('account_id.id', '=', record_id),
                ('date_from', '<=', dt_from),
                '|', ('date_to', '>=', dt_to),
                ('date_to', '=', False)]

            interest_ids = interest_obj.search(
                cr, uid, interest_domain, context=context)

            if interest_ids:
                res[record_id] = interest_obj.browse(
                    cr, uid, interest_ids[0], context=context)
        return res
