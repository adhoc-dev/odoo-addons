# -*- coding: utf-8 -*-


from openerp.osv import osv, fields

class account_journal(osv.osv):
    _inherit = 'account.journal'
    _columns = {
    	'check_type': fields.selection([('issue', 'Issue'),('third', 'Third')], 'Check Type', help='Choose check type, if none check journal then keep it empty.'),      	
        'validate_only_checks': fields.boolean('Validate only Checks', help='If marked, when validating a voucher, verifies that the total amounth of the voucher is the same as the checks used.'),
        'checkbook_ids': fields.one2many('account.checkbook','journal_id','Checkbooks',),
    }
