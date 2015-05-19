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
        return [('cash', _('Cash Payment')),
                ('bank', _('Bank'))]

    payment_method = fields.Selection('_get_payment_method', string='Payment Method')

    @api.model
    def check_payment_method(self, type, payment_method):
        if (type == 'cash' and payment_method != 'cash') \
                or (type != 'cash' and payment_method == 'cash'):
            raise except_orm(_('Warning!'), _('Cash payment method is used in Cash type journal!'))
        if (type not in ('cash', 'bank') and payment_method \
                or (type in ('cash', 'bank') and not payment_method)):
            raise except_orm(_('Warning!'), _('Payment method is used in Cash and Bank journals!'))

    @api.model
    def create(self, values):
        if values['type'] == 'bank' and 'payment_method' not in values:
            values['payment_method'] = 'bank'
        if values['type'] == 'cash' and 'payment_method' not in values:
            values['payment_method'] = 'cash'
        self.check_payment_method(values['type'], values['payment_method'])
        return super(AccountJournal, self).create(values)

    @api.multi
    def write(self, values, context=None):
        res = super(AccountJournal, self).write(values)
        for journal in self.browse(self.ids):
            self.check_payment_method(journal.type, journal.payment_method)
        return res

class AccountMove(models.Model):
    _inherit = "account.move"

    payment_method = fields.Selection(related='journal_id.payment_method', string='Payment Method', readonly=True )

