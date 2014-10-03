# -*- coding: utf-8 -*-
from openerp import models


class ir_actions_report(models.Model):
    _inherit = 'ir.actions.report.xml'

    def get_domains(self, cr, model, record, context=None):
        domains = super(ir_actions_report, self).get_domains(
            cr, model, record, context=context)
        if model == 'purchase.order':
            # No rules
            domains.append([])
        return domains
