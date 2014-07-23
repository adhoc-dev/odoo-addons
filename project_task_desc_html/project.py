# -*- coding: utf-8 -*-
from openerp import models, fields

class task(models.Model):
    """"""
    
    _inherit = 'project.task'

    description = fields.Html('Description')