# -*- coding: utf-8 -*-
##############################################################################
#
#    Ingenieria ADHOC - ADHOC SA
#    https://launchpad.net/~ingenieria-adhoc
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.tools.translate import _
from openerp.osv import fields, osv

class account_invoice(osv.osv):

    _name = "account.invoice"
    _inherit = 'account.invoice'

    _columns = {
		'sequence_id': fields.related('journal_id', 'sequence_id', type='many2one', string='Sequence', readonly=True, relation="ir.sequence"),
		'next_invoice_number': fields.related('sequence_id', 'number_next', type='integer', string='Next Invoice Number', readonly=True),
    }
