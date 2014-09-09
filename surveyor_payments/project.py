 #-*- coding: utf-8 -*-
from openerp import fields, models, api


class project_task_payment(models.Model):
    _name = 'project.task.payment'
    # _order = 'date desc'
    _rec_name = 'description'

    task_id = fields.Many2one('project.task', 'Task', required=True)
    description = fields.Char('Description')
    date = fields.Date(
        'Fecha',
        default=lambda self: fields.date.today(),
        required=True)
    amount = fields.Float('Amount', required=True)


class project_task(models.Model):
    _inherit = 'project.task'

    @api.one
    @api.depends('payment_ids', 'payment_ids.amount', 'total_amount')
    def _get_balance_amount(self):
        balance_amount = False
        if self.total_amount:
            total_paid = sum([x.amount for x in self.payment_ids])
            balance_amount = self.total_amount - total_paid
        self.balance_amount = balance_amount

    total_amount = fields.Float('Total Amount')
    balance_amount = fields.Float(
        'Balance Amount',
        compute='_get_balance_amount',
        store=True)
    payment_ids = fields.One2many(
        'project.task.payment',
        'task_id',
        'Payments')
    payment_term_id = fields.Many2one(
        'account.payment.term',
        string='Payment Terms')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
