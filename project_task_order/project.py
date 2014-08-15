 #-*- coding: utf-8 -*-
from openerp import fields, models

class project_task(models.Model):
    _inherit = 'project.task'
    _order = "priority desc, sequence, date_deadline, planned_hours, date_start, create_date desc"

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
