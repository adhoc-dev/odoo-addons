# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015, Eska Yazılım ve Danışmanlık A.Ş.
#    http://www.eskayazilim.com.tr
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

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    @api.model
    def _get_payment_method(self):
        return [('none', _('None')),
                ('cash', _('Cash Payment')),
                ('bank', _('Bank'))]

    payment_method = fields.Selection('_get_payment_method', string='Payment Method', required=True, default='none')

    @api.multi
    def write(self, values, context=None):
        res = super(AccountJournal, self).write(values)
        for journal in self.browse(self.ids):
            if (journal.type == 'cash' and journal.payment_method != 'cash') \
                    or (journal.type != 'cash' and journal.payment_method == 'cash'):
                raise except_orm(_('Warning!'), _('Cash payment method is used in Cash type journal!'))
            if journal.type not in ('cash', 'bank') and journal.payment_method != 'none':
                raise except_orm(_('Warning!'), _('Payment method is used in Cash and Bank journals!'))
        return res



class AccountMove(models.Model):
    _inherit = "account.move"

    payment_method = fields.Selection(related='journal_id.payment_method', string='Payment Method', readonly=True )

