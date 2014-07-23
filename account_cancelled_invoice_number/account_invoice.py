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

from openerp import netsvc
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _

class account_invoice(osv.osv):

    _name = "account.invoice"
    _inherit = 'account.invoice'

    _columns = {
#        'number': fields.related('internal_number', type='char', readonly=True, size=32, store=True, string='Number')
#		'number': fields.related('self', 'internal_number', type='char', string='Number')
#		'number': fields.related('internal_number', type='char', string='Number')        
        'number': fields.related('internal_number', type='char', readonly=True, size=64, store=True, string='Number'),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
