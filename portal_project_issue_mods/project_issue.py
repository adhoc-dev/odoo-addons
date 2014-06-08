 #-*- coding: utf-8 -*-
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

from openerp.osv import fields, osv, orm

class project_issue(osv.osv):
    _name = "project.issue"
    _description = "Project Issue"
    _inherit = 'project.issue'

    def case_open(self, cr, uid, ids, context=None):
        if not isinstance(ids,list): ids = [ids]
        return self.case_set(cr, 1, ids, 'open', {'date_start': fields.datetime.now()}, context=context)

    _columns = {
    }

# Modification so that when we change project it also change user
    def on_change_project(self, cr, uid, ids, project_id, context=None):
        if project_id:
            project = self.pool.get('project.project').browse(cr, uid, project_id, context=context)
            ret = {}
            if project and project.user_id:
                ret =  {'value': {'user_id': project.user_id.id}}              
            if project and project.partner_id:
                ret =  {'value': {'partner_id': project.partner_id.id}}              
        return ret

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
