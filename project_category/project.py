# -*- coding: utf-8 -*-
from openerp import models, fields


class project_category(models.Model):

    _name = 'project.type'
    _description = 'Project Category'

    name = fields.Char(
        'Category Name',
        required=True
    )
    description = fields.Text('Description')


class project(models.Model):

    _inherit = 'project.project'

    type_id = fields.Many2one(
        'project.type',
        'Category',
        copy=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
