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

class project_isssue_solution(osv.osv):
    """ Note """
    _name = 'project.issue.solution'
    _inherit = ['mail.thread']
    _description = "Project Issue Solution"
    _order = 'name'

    _columns = {
        'name': fields.char(string='Name', required=True),
        'solution_description': fields.text('Solution Description'),
        'issue_description': fields.text('Issue Description'),
		'categ_ids': fields.many2many('project.category', string='Tags'),        
        'project_issue_ids': fields.one2many('project.issue', 'project_issue_solution_id', string='Issues'),        
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
