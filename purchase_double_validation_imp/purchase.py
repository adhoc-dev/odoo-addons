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

from openerp.osv import fields, osv
from openerp import netsvc
from openerp import pooler
from openerp.tools.translate import _

class purchase_order(osv.osv):

    _inherit = "purchase.order"

    def print_order(self, cr, uid, ids, context=None):
        '''
        This function prints the request for order
        '''
        # assert len(ids) == 1, 'This option should only be used for a single id at a time'
        # wf_service = netsvc.LocalService("workflow")
        # wf_service.trg_validate(uid, 'purchase.order', ids[0], 'send_rfq', cr)
        datas = {
                 'model': 'purchase.order',
                 'ids': ids,
                 'form': self.read(cr, uid, ids[0], context=context),
        }
        return {'type': 'ir.actions.report.xml', 'report_name': 'purchase.order', 'datas': datas, 'nodestroy': True}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
