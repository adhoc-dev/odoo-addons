# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp.osv import osv, fields

class users(osv.osv):
    _name = 'res.users'
    _inherit = 'res.users'
    
    _columns = {
        'journal_ids': fields.many2many('account.journal', 'journal_security_journal_users','user_id',
                                        'journal_id', 'Restricted Journals', help="This journals and the information related to it will be only visible for users where you specify that they can see them setting this same field."),
    }