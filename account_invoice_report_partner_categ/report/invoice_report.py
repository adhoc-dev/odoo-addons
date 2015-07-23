# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class account_invoice_report(models.Model):
    _inherit = 'account.invoice.report'

    partner_category_ids = fields.Many2many(
        'res.partner.category',
        string='Partner Category',
        related='partner_id.category_id'
        )
