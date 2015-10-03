# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import api, fields, models
from openerp.tools.translate import _


class AccountJournalEntriesReport(models.TransientModel):
    _name = "account.journal.entries.report"
    _description = "Print journal by entries"

    company_id = fields.Many2one(
        'res.company',
        default=lambda self: self.env.user.company_id,
        required=True,
        )
    fiscalyear_id = fields.Many2one(
        'account.fiscalyear',
        'Fiscal Year',
        required=True,
        ondelete='cascade',
        domain="[('company_id', '=', company_id)]",
        )
    journal_ids = fields.Many2many(
        'account.journal',
        'account_journal_entries_journal_rel',
        'acc_journal_entries_id',
        'journal_id',
        'Journals',
        required=True,
        ondelete='cascade',
        )
    period_ids = fields.Many2many(
        'account.period',
        'account_journal_entries_account_period_rel',
        'acc_journal_entries_id', 'account_period_id',
        'Period'
        )
    sort_selection = fields.Selection(
        [('date', 'By date'),
         ('name', 'By entry number'),
         ('ref', 'By reference number')],
        'Entries Sorted By',
        required=True,
        default='name',
        )
    landscape = fields.Boolean(
        'Landscape mode',
        default=True,
        )

    @api.onchange('fiscalyear_id')
    def change_fiscalyear(self):
        self.period_ids = self.period_ids.search([
            ('fiscalyear_id', '=', self.fiscalyear_id.id)])

    @api.onchange('company_id')
    def change_company(self):
        # domain = []
        # if self.company_id:
            # domain.append(('company_id', '=', self.company_id.id))
        domain = [('company_id', '=', self.company_id.id)]
        self.fiscalyear_id = self.fiscalyear_id.with_context(
            company_id=self.company_id.id).find()
        self.journal_ids = self.journal_ids.search(domain)

    @api.multi
    def _check_data(self):
        self.ensure_one()
        if not self.period_ids and not self.journal_ids:
            return False
        for journal in self.journal_ids:
            for period in self.period_ids:
                journal_periods = self.env['account.journal.period'].search(
                    [('journal_id', '=', journal.id),
                        ('period_id', '=', period.id)])
                if journal_periods:
                    return True
        return False

    @api.multi
    def _check(self):
        self.ensure_one()
        return 'report_landscape' if self.landscape else 'report'

    @api.multi
    def print_report(self):
        """Print report."""
        self.ensure_one()
        data = self.read()[0]
        datas = {
            'ids': self._context.get('active_ids', []),
            'model': 'ir.ui.menu',
            'form': data,
        }
        if not self._check_data():
            raise Warning(_(
                'No data available!\n'
                'No records found for your selection!'))
        if self._check() == 'report_landscape':
            report_name = 'account.journal.entries.report.wzd1'
        else:
            report_name = 'account.journal.entries.report.wzd'
        return {
            'type': 'ir.actions.report.xml',
            'report_name': report_name,
            'datas': datas,
            'context': self._context,
        }
