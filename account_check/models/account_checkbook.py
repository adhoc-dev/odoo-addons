# -*- coding: utf-8 -*-
from openerp import fields, models, api, _
import logging
_logger = logging.getLogger(__name__)


class account_checkbook(models.Model):

    _name = 'account.checkbook'
    _description = 'Account Checkbook'
    _inherit = ['mail.thread']

    @api.one
    def _get_next_check_number(self):
        next_number = self.range_from
        check_numbers = [
            check.number for check in self.issue_check_ids]
        if check_numbers:
            next_number = max(check_numbers) + 1
        self.next_check_number = next_number

    name = fields.Char(
        'Name', size=30, readonly=True, required=True,
        states={'draft': [('readonly', False)]})
    issue_check_subtype = fields.Selection(
        [('deferred', 'Deferred'), ('currents', 'Currents')],
        string='Issue Check Subtype', readonly=True, required=True,
        help='The only difference bewteen Deferred and Currents is that when delivering a Deferred check a Payment Date is Require',
        states={'draft': [('readonly', False)]})
    debit_journal_id = fields.Many2one(
        'account.journal', 'Debit Journal',
        help='It will be used to make the debit of the check on checks ', readonly=True, required=True,
        domain=[('type', '=', 'bank')], context={'default_type': 'bank'},
        states={'draft': [('readonly', False)]})
    journal_id = fields.Many2one(
        'account.journal', 'Journal',
        help='Journal where it is going to be used',
        readonly=True, required=True, domain=[('type', '=', 'bank')],
        context={'default_type': 'bank'},
        states={'draft': [('readonly', False)]})
    range_from = fields.Integer(
        'From Check Number', readonly=True, required=True,
        states={'draft': [('readonly', False)]})
    range_to = fields.Integer(
        'To Check Number', readonly=True, required=True,
        states={'draft': [('readonly', False)]})
    next_check_number = fields.Char(
        compute='_get_next_check_number',
        string='Next Check Number',)
    padding = fields.Integer(
        'Number Padding', default=8,
        help="automatically adds some '0' on the left of the 'Number' to get the required padding size.")
    company_id = fields.Many2one(
        'res.company',
        related='journal_id.company_id',
        requirde=True, readonly=True,
        string='Company', store=True)
    issue_check_ids = fields.One2many(
        'account.check', 'checkbook_id', string='Issue Checks', readonly=True,)
    state = fields.Selection(
        [('draft', 'Draft'), ('active', 'In Use'), ('used', 'Used')],
        string='State', readonly=True, default='draft')

    _order = "name"

    def _check_numbers(self, cr, uid, ids, context=None):
        record = self.browse(cr, uid, ids, context=context)
        for data in record:
            if (data.range_to <= data.range_from):
                return False
        return True

    _constraints = [
        (_check_numbers, 'Range to must be greater than range from',
         ['range_to', 'range_from']),
    ]

    @api.one
    @api.constrains('debit_journal_id', 'journal_id')
    def check_journals(self):
        if self.journal_id.company_id != self.debit_journal_id.company_id:
            raise Warning(
                _('Journal And Debit Journal must belong to the same company'))

    def copy(self, cr, uid, id, default=None, context=None):
        default = {} if default is None else default.copy()
        context = {} if context is None else context.copy()
        record = self.browse(cr, uid, id, context=context)
        default.update({
            'state': 'draft',
            'ref': False,
            'name': _("%s (copy)") % (record.name or ''),
        })
        return super(account_checkbook, self).copy(cr, uid, id, default, context)

    def unlink(self, cr, uid, ids, context=None):
        for record in self.browse(cr, uid, ids, context=context):

            if record.state not in ('draft'):
                raise Warning(
                    _('You can drop the checkbook(s) only in draft state !'))
                return False
        return super(account_checkbook, self).unlink(cr, uid, ids, context=context)

    def wkf_active(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            if res:
                raise Warning(_(
                    'You cant change the checkbook´s state, there is one active for this Bank Account!'))
                return False
            else:
                self.write(cr, uid, ids, {'state': 'active'})
                return True

    def wkf_used(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'used'})
        return True

    def action_cancel_draft(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state': 'draft'})
        self.delete_workflow(cr, uid, ids)
        self.create_workflow(cr, uid, ids)
