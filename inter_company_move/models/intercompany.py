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

from openerp.osv import osv, fields
from openerp.tools.translate import _

class intercompany_document(osv.osv):
    _name = 'intercompany.document'
    _description = 'Intercompany Document'

    _columns = {
        'company_id': fields.many2one('res.company', 'Company', required=True, ondelete="cascade",),
        'model': fields.selection([('invoice','Invoice')], string='Model', required=True),
        # 'model_id': fields.many2one('account.model', 'Model', required=True, ondelete="cascade", ),
        'type': fields.selection([('move_auto','Move Automatically'),('move_wizard','Move With Wizard')], string='Type', required=True),
        'destiny_company_id': fields.many2one('res.company', 'Destiny Company',),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
