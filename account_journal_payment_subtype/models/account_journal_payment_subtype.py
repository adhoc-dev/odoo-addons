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

    payment_subtype = fields.Selection(
        '_get_payment_subtype',
        string='Payment Subtype'
        )


class AccountVoucher(models.Model):
    _inherit = 'account.voucher'

    payment_subtype = fields.Selection(
        related='journal_id.payment_subtype',
        string='Payment Subtype', readonly=True,
        )
