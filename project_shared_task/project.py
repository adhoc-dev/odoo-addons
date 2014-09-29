# -*- coding: utf-8 -*-


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


