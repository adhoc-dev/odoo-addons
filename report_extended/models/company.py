# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class res_company(models.Model):
    _inherit = 'res.company'

    report_company_name = fields.Char(
        'Report Company Name', help='Company name to be printed on reports',)
