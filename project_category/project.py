# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class project_type(models.Model):

    _name = 'project.type'
    _description = 'Project Type'

    name = fields.Char(
        'Name',
        required=True
    )
    description = fields.Text('Description')


class project(models.Model):

    _inherit = 'project.project'

    type_id = fields.Many2one(
        'project.type',
        'Type',
        copy=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
