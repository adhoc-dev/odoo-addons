# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class project_tag(models.Model):

    _name = 'project_tags.project_tag'
    _description = 'project_tag'

    name = fields.Char(string='Name', required=True, size=64)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
