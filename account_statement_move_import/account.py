# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api,  _
from openerp.exceptions import Warning


class account_move_line(models.Model):
    _inherit = 'account.move.line'

    exclude_on_statements = fields.Boolean(
        'Exclude on Statements',
        help='Exclude this move line suggestion on statements',
        )


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
        # search if this moveline has been imported
        # TODO when removing imported field, we should search directly for
        # lines by o2m to imported_line_id
        statement_lines = statement_lines.sudo().search([
                ('journal_entry_id', 'in', self.ids),
                ('imported', '=', True),
                ])
        if statement_lines:
            raise Warning(_(
                "You can not cancel an Accounting Entry that is linked "
                "to a statement. You should cancel or delete lines from "
                "statement first. Related Statements: '%s'") % (
                    ', '.join(statement_lines.mapped('statement_id.name'))))
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

    imported_line_id = fields.Many2one(
        'account.move.line',
        'Imported Move Line',
        readonly=True,
        help='Imported lines are the ones imported by the '
        '"Import Journal Items" wizard. They have some special behaviour, '
        'for eg. you can not cancel them from here',
        )
    imported = fields.Boolean(
        'Imported?',
        # TODO remove this field on v9, we keep because we use it before adding
        # imported_line_id field
        depreceated=True,
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
            # TODO remove "not r.imported_line_id" when depreceating
            # imported field
            return super(account_bank_statement_line, self.filtered(
                lambda r: not r.imported_line_id and not r.imported)).cancel()
        for line in self:
            # TODO remove "or line.imported" when depreceating imported field
            if line.imported_line_id or line.imported:
                raise Warning(_(
                    'You can not cancel line "%s" as it has been imported with'
                    ' "Import Journal Items" wizard, you can delete it '
                    'instead') % ('%s - %s' % (line.name, line.ref or '')))
        return super(account_bank_statement_line, self.with_context(
            cancel_from_statement_line=True)).cancel()

    @api.multi
    def unlink(self):
        for line in self:
            if line.imported_line_id:
                # First remove journal_entry_id id in order to avoid constraint
                # and let unlink imported lines
                line.imported_line_id.statement_id = False
                line.journal_entry_id = False
            # TODO remove this elif when depreceating imported field
            elif line.imported:
                line.journal_entry_id.line_id.write({'statement_id': False})
                line.journal_entry_id = False
        return super(account_bank_statement_line, self).unlink()
