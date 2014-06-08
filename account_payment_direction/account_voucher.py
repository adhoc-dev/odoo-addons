# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

import logging
from datetime import datetime
import time

from openerp import SUPERUSER_ID
from openerp.osv import fields, osv
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)


class account_journal(osv.osv):
    _inherit = "account.voucher"    

    _columns = {
        'in_journal_id': fields.related('journal_id', type="many2one", relation="account.journal", string="Journal",),
        'out_journal_id': fields.related('journal_id', type="many2one", relation="account.journal", string="Journal",),
    }

    def onchange_copy_journal(self, cr, uid, ids, out_journal_id, in_journal_id, context=None):
        if context is None:
            context = {}

        if out_journal_id:
        	journal_id = out_journal_id
    	elif in_journal_id:
        	journal_id = in_journal_id
    	else:
        	journal_id = False

        vals = {'value':{} }
        vals['value'].update({'journal_id': journal_id})

        return vals

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
