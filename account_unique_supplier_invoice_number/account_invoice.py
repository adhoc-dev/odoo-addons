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

from openerp.osv import osv

class account_invoice(osv.osv):
    _inherit = 'account.invoice'

    _sql_constraints = [
        ('number_supplier_invoice_number', 'unique(supplier_invoice_number, partner_id)', 'Supplier Invoice Number must be unique per Supplier!'),
    ]

    def copy(self, cr, uid, id, default=None, context=None):
        default = default or {}
        default.update({
            'supplier_invoice_number':False,
        })
        return super(account_invoice, self).copy(cr, uid, id, default, context)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
