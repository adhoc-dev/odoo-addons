# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields

class task(models.Model):
    """"""
    
    _inherit = 'project.task'

    description = fields.Html('Description')