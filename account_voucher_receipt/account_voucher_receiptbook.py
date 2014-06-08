# -*- coding: utf-8 -*-
##############################################################################
#
#    Ingenieria ADHOC - ADHOC SA
#    https://launchpad.net/~ingenieria-adhoc
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
import logging
import time
_logger = logging.getLogger(__name__)
from openerp.tools.translate import _
from datetime import datetime

class account_voucher_receiptbook(osv.osv):
    
    _name = 'account.voucher.receiptbook'
    _description = 'Account Voucher Receiptbook'

    _columns = {
        'sequence': fields.integer('Sequence', help="Used to order the receiptbooks"),
        'name':fields.char('Name', size=64, readonly=False,required=True,),
        'type':fields.selection([('receipt','Receipt'),('payment','Payment')], string='Type', readonly=False, required=True, ),
        'sequence_type':fields.selection([('automatic','Automatic'),('manual','Manual')], string='Sequence Type', readonly=False, required=True, ),
        'sequence_id': fields.many2one('ir.sequence', 'Entry Sequence', help="This field contains the information related to the numbering of the receipt entries of this receiptbook.", required=False),
        'company_id': fields.many2one('res.company', 'Company', required=True, ),
        'manual_prefix': fields.char('Prefix',),
        'padding' : fields.integer('Number Padding', help="automatically adds some '0' on the left of the 'Number' to get the required padding size."),
        'active': fields.boolean('Active',),
    }

    _order = 'sequence asc'

    _defaults = {
        'active': True, 
        'sequence' : 1,
        'sequence_type': 'automatic',
        'company_id': lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, 'account.voucher.receipt',context=c),
    }    

    def copy(self, cr, uid, id, default=None, context=None):
        default = {} if default is None else default.copy()
        default.update(
            sequence_id=False)
        return super(account_voucher_receiptbook, self).copy(cr, uid, id, default, context=context)