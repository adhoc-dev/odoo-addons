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
    def _get_payment_subtype(self):
        return []

    payment_subtype = fields.Selection('_get_payment_subtype', string='Payment Subtype')

    # @api.model
    # def check_payment_subtype(self, type, payment_subtype):
    #     if (type == 'cash' and payment_subtype != 'cash') \
    #             or (type != 'cash' and payment_subtype == 'cash'):
    #         raise except_orm(_('Warning!'), _('Cash Payment Subtype is used in Cash type journal!'))
    #     if (type not in ('cash', 'bank') and payment_subtype \
    #             or (type in ('cash', 'bank') and not payment_subtype)):
    #         raise except_orm(_('Warning!'), _('Payment Subtype is used in Cash and Bank journals!'))

    # @api.model
    # def create(self, values):
    #     if values['type'] == 'bank' and 'payment_subtype' not in values:
    #         values['payment_subtype'] = 'bank'
    #     if values['type'] == 'cash' and 'payment_subtype' not in values:
    #         values['payment_subtype'] = 'cash'
    #     self.check_payment_subtype(values['type'], values['payment_subtype'])
    #     return super(AccountJournal, self).create(values)

    # @api.multi
    # def write(self, values, context=None):
    #     res = super(AccountJournal, self).write(values)
    #     for journal in self.browse(self.ids):
    #         self.check_payment_subtype(journal.type, journal.payment_subtype)
    #     return res
