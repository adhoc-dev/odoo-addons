# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp.osv import fields, osv, expression

class account_journal(osv.osv):
    _inherit = "account.journal"
    _columns = {
        'sequence': fields.integer('Sequence', help="Gives the sequence order when selecting a journal."),
    }
    _defaults = {
        'sequence': 10,
    }
    _order = "sequence"

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
