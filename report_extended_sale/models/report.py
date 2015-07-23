# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class ir_actions_report(models.Model):
    _inherit = 'ir.actions.report.xml'

    sale_order_state = fields.Selection(
        [('draft', 'Quotation'), ('progress', 'In Progress')],
        'Sale Order State', required=False)

    def get_domains(self, cr, model, record, context=None):
        domains = super(ir_actions_report, self).get_domains(
            cr, model, record, context=context)
        if record.state in ['draft', 'sent']:
            sale_order_state = 'draft'
        else:
            sale_order_state = 'progress'
        if model == 'sale.order':
            # Search for especific report
            domains.append([('sale_order_state', '=', sale_order_state)])
            # Search without state defined
            domains.append([('sale_order_state', '=', False)])
        return domains
