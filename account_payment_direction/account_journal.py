# -*- coding: utf-8 -*-


import logging
from datetime import datetime
import time

from openerp import SUPERUSER_ID
from openerp.osv import fields, osv
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)


class account_journal(osv.osv):
    _name = "account.journal"
    _inherit = "account.journal"    
    _columns = {
        'direction': fields.selection([('in', 'In'),('out','Out')], 'Direction', size=32, required=False,
                                 help="Select 'In' for customer payments."\
                                 " Select 'Out' for supplier payments."),
    }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
