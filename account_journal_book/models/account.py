# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import fields, models, api
import logging

_logger = logging.getLogger(__name__)


class account_move(models.Model):
    _inherit = 'account.move'

    number_in_book = fields.Char(
        string='Number in Book',
        help='This number is set when closing a period or by running a wizard'
        )

    _sql_constraints = [
        ('number_in_book_uniq', 'unique(number_in_book, company_id)',
            'Number in Book must be unique per Company!')]

    @api.multi
    def moves_renumber(self, sequence):
        _logger.info("Renumbering %d account moves.", len(self.ids))
        for move in self:
            new_number = sequence.with_context(
                fiscalyear_id=move.period_id.fiscalyear_id.id)._next()
            move.number_in_book = new_number
