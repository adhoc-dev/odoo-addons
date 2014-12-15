# -*- coding: utf-8 -*-
from openerp import models, fields


class project(models.Model):
    _inherit = 'project.project'

    project_tag_ids = fields.Many2many(
        'project_tags.project_tag',
        'project_project_tag_ids_rel',
        'project_id',
        'project_tag_id',
        string='Tags')
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
