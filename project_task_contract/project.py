# -*- coding: utf-8 -*-
from openerp import models, fields, api


class account_analytic_account(models.Model):
    _inherit = 'account.analytic.account'

    task_project_type = fields.Selection(
        [('contract_project', 'Contract Own Project'),
         ('other_project', 'Other Project')],
        'Project Type',
        default='contract_project')
    other_project_id = fields.Many2one(
        'project.project',
        'Other Project')
    other_project_task_ids = fields.One2many(
        'project.task', 'analytic_account_id', 'Tasks')
    task_count = fields.Integer(
        compute='_task_count', string="Tasks",)

    @api.one
    @api.depends('other_project_task_ids')
    def _task_count(self):
        self.task_count = len(self.other_project_task_ids)

    @api.onchange('use_tasks')
    def change_use_tasks(self):
        if not self.use_tasks:
            self.other_project_id = False
            self.task_project_type = False

    def _trigger_project_creation(self, cr, uid, vals, context=None):
        '''
        This function is used to decide if a project needs to be automatically created or not when an analytic account is created. It returns True if it needs to be so, False otherwise.
        '''
        if vals.get('task_project_type') != 'contract_project':
            return False
        return super(account_analytic_account, self)._trigger_project_creation(
            cr, uid, vals, context)

    def on_change_template(
            self, cr, uid, ids, template_id, date_start=False, context=None):
        res = super(account_analytic_account, self).on_change_template(
            cr, uid, ids, template_id, date_start=date_start, context=context)
        if template_id and 'value' in res:
            template = self.browse(cr, uid, template_id, context=context)
            res['value']['task_project_type'] = template.task_project_type
            res['value']['other_project_id'] = template.other_project_id
        return res


class project(models.Model):
    _inherit = 'project.task'

    analytic_account_id = fields.Many2one(
        'account.analytic.account', 'Contract/Analytic',
        help="Link this task to an analytic account if you need financial management on tasks. "
             "It enables you to connect tasks with budgets, planning, cost and revenue analysis, timesheets on task, etc.",
        ondelete="cascade",
        domain=[('type', '=', 'contract'), ('state', 'in', ['open'])],
        auto_join=True)

    @api.onchange('analytic_account_id')
    def change_analytic_account_id(self):
        if self.analytic_account_id:
            self.project_id = self.analytic_account_id.other_project_id
            self.partner_id = self.analytic_account_id.partner_id
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
