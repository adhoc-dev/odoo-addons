# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

class account_journal(osv.osv):
    _name = 'account.journal'
    _inherit = 'account.journal'
    
    _columns = {
        'user_ids': fields.many2many('res.users', 'journal_security_journal_users', 'journal_id', 
    		'user_id', string='Restricted to Users', help='If choose some users, then this journal and the information related to it will be only visible for those users.'),
    }