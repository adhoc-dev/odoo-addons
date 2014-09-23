# -*- coding: utf-8 -*-
from openerp import models, fields


class ir_actions_report(models.Model):
    _inherit = 'ir.actions.report.xml'

    sale_order_state = fields.Selection(
        [('draft', 'Quotation'), ('progress', 'In Progress')],
        'Sale Order State', required=False),

    def get_domains(self, cr, model, record, context=None):
        domains = super(ir_actions_report, self).get_domains(
            cr, model, record, context=context)
        if model == 'purchase.order':
            # No rules
            domains.append([])
        return domains
