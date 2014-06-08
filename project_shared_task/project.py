# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Eficent (<http://www.eficent.com/>)
#              Jordi Ballester Alomar <jordi.ballester@eficent.com>
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

import tools
from osv import fields, osv
from tools.translate import _


class task(osv.osv):
    _inherit = 'project.task'
    
    _columns = {
        'members': fields.many2many('res.users', 'task_user_rel', 'task_id', 'uid', 'Task Members',
            help="Task's members are users who can edit some fields on this task.", states={'done':[('readonly',True)], 'cancelled':[('readonly',True)]}),
    }

class project_work(osv.osv):
    _inherit = "project.task.work"

    def write(self, cr, uid, ids, vals, context=None):
        """
        We change the user id so that it doenst gives error 
        """
        uid = 1 
        return super(project_work,self).write(cr, uid, ids, vals, context)


