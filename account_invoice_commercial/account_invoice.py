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

from openerp.osv import osv, fields
from openerp import netsvc

class account_invoice(osv.osv):

    _name = 'account.invoice'
    _inherit = 'account.invoice'


    def onchange_partner_id(self, cr, uid, ids, type, partner_id, date_invoice=False, payment_term=False, partner_bank_id=False, company_id=False):
        ret = super(account_invoice, self).onchange_partner_id(cr, uid, ids, type, partner_id, date_invoice, payment_term, partner_bank_id, company_id)

        if not ret.has_key('value'):
            ret['value'] = {}
        
        if partner_id:
            res_partner_obj = self.pool.get('res.partner')
            partner = res_partner_obj.browse(cr, uid, partner_id, context=None)
            ret['value'] = {
            'user_id': partner.user_id.id or uid,
            }
        else:
            ret['value'] = {
            'user_id': uid,
            }

        return ret


account_invoice() 