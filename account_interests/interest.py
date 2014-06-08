# -*- coding: utf-8 -*-
##############################################################################
#
#    Ingenieria ADHOC - ADHOC SA
#    https://launchpad.net/~ingenieria-adhoc
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

from openerp.osv import fields, osv
#import decimal_precision as dp

# import re  
from openerp.tools.translate import _
        
        
#----------------------------------------------------------
#  generel Interest
#----------------------------------------------------------

# class account_company_interest(osv.osv):
#     _name = "account.company.interest"
#     _description = 'Account Company Interest'
#     _columns = {
#         'company_id': fields.many2one('res.company', 'Company'), 
#         'name'      : fields.char('Interest Name', size=32),
#         'interest_rate_ids' : fields.one2many('account.company.interest.rate', 'company_interest_rate_id', 'Interest Rates'),
#     }
     

# class account_company_interest_rate(osv.osv):
#     _name = "account.company.interest.rate"
#     _description = 'Account Company Interest Rate'
#     _columns = {
#         'company_interest_rate_id': fields.many2one('account.company.interest', 'Interest Rate'),     
#         'interest_rate_debit': fields.float('Interest Debit', required=True,   digits=(7,4)),
#         'interest_rate_credit': fields.float('Interest Credit', required=True,  digits=(7,4) ),
#         'date_from': fields.date('Date From',required=True),
#         'date_to': fields.date('Date To'),
#      }

#----------------------------------------------------------
#  Account specific Interest
#----------------------------------------------------------
class account_account_interest(osv.osv):
    _name = "account.account.interest"
    _description = 'Account Account Interest'
    _columns = {
        # 'company_id': fields.many2one('res.company', 'Company'),     
        'account_id': fields.many2one('account.account', 'Account', required=True, ondelete="cascade"),
        'interest_account_id': fields.many2one('account.account', 'Interest Account', required=True, domain=[('type','!=', 'view')]),
        'analytic_account_id': fields.many2one('account.analytic.account', 'Analytic account', domain=[('type','!=', 'view')]),
        'interest_rate': fields.float('Interest', required=True,  digits=(7,4)),
        # 'interest_rate_debit': fields.float('Interest Debit', required=True,   digits=(7,4)),
        # 'interest_rate_credit': fields.float('Interest Credit', required=True,  digits=(7,4) ),
        'date_from': fields.date('Date From',required=True),
        'date_to': fields.date('Date To'),
     }

class account_account(osv.osv):
    _inherit = "account.account"
    _columns = {
         # 'account_interest_ids'         : fields.many2many('account.company.interest','account_company_interest_rel','account_id','account_company_interest_id', 'General Interest Rates'),
         'account_account_interest_ids' : fields.one2many('account.account.interest', 'account_id', 'Interest Rates'),
    }

    def get_active_interest_data(self, cr, uid, ids, dt_from, dt_to, context=None):
        if context is None:
            context = {}        
        interest_obj = self.pool.get('account.account.interest')
        res = {}

        for record_id in ids:
            interest_domain = [('account_id.id','=',record_id), ('date_from', '<=', dt_from), '|', ('date_to', '>=', dt_to), ('date_to', '=', False)]
            interest_ids = interest_obj.search(cr, uid, interest_domain, context=context)
            if interest_ids:               
                res[record_id] = interest_obj.browse(cr, uid, interest_ids[0], context=context)
        return res
