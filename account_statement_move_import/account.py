# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api,  _
from openerp.exceptions import Warning


class account_move(models.Model):
    _inherit = 'account.move'

    @api.multi
    def button_cancel(self):
        """
        If cancel is called form a statement, then we cancel without checks.
        If not, we only cancel if line is not linked to a statement.
        """
        if self._context.get('cancel_from_statement_line', False):
            return super(account_move, self).button_cancel()

        statement_lines = self.env['account.bank.statement.line']
        # run with sudo because we may not have access to statement line
        statement_lines = statement_lines.sudo().search([
                ('journal_entry_id', 'in', self.ids)])
        if statement_lines:
            raise Warning(_(
                "You can not cancel an Accounting Entry that is linked "
                "to a statement. You should cancel or delete lines from "
                "statement first. Related Statements: '%s'" % (
                    ', '.join(statement_lines.statement_id.mapped('name')))))
        else:
            return super(account_move, self).button_cancel()


class account_bank_statement(models.Model):
    _inherit = 'account.bank.statement'

    @api.multi
    def button_cancel(self):
        return super(account_bank_statement, self.with_context(
            cancel_from_statement=True)).button_cancel()


class account_bank_statement_line(models.Model):
    _inherit = 'account.bank.statement.line'

    imported = fields.Boolean(
        'Imported?',
        readonly=True,
        help='Imported lines are the ones imported by the '
        '"Import Journal Items" wizard. They have some special behaviour, '
        'for eg. you can not cancel them from here',
        )

    @api.multi
    def cancel(self):
        # if we are canceling the statement then we dont raise the warning
        # and return cancellation only for none imported lines
        if self._context.get('cancel_from_statement', False):
            super(account_bank_statement_line, self.filtered(
                lambda r: not r.imported)).cancel()
        for line in self:
            if line.imported:
                raise Warning(_(
                    'You can not cancel line "%s" as it has been imported with'
                    ' "Import Journal Items" wizard, you can delete it '
                    'instead') % ('%s - %s' % (line.name, line.ref or '')))
        return super(account_bank_statement_line, self.with_context(
            cancel_from_statement_line=True)).cancel()

    @api.multi
    def unlink(self):
        for line in self:
            if line.imported:
                # First remove journal_entry_id id in order to avoid constraint
                # and let unlink imported lines
                line.journal_entry_id.line_id.write({'statement_id': False})
                line.journal_entry_id = False
        return super(account_bank_statement_line, self).unlink()
