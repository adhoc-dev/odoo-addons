 #-*- coding: utf-8 -*-
from openerp import fields, models

class project_issue(models.Model):
    _inherit = 'project.issue'
    _order = "priority desc, sequence, date_deadline, duration, create_date desc"

    sequence = fields.Integer('Sequence', select=True, default=10, help="Gives the sequence order when displaying a list of tasks.")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
