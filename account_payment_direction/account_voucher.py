# -*- coding: utf-8 -*-


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
