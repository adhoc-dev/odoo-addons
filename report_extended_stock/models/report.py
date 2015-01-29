# -*- coding: utf-8 -*-
from openerp import models, fields


class ir_actions_report(models.Model):
    _inherit = 'ir.actions.report.xml'

    stock_picking_type_ids = fields.Many2many(
        'stock.picking.type',
        'report_configuration_stock_picking_type_rel',
        'report_configuration_id', 'picking_type_id', 'Picking Types')
    stock_report_type = fields.Selection(
        [('voucher', 'Voucher'), ('picking_list', 'Picking List')],
        'Stock Report Type',)

    def get_domains(self, cr, model, record, context=None):
        domains = super(ir_actions_report, self).get_domains(
            cr, model, record, context=context)
        if model == 'stock.picking':
            stock_report_type = context.get('stock_report_type', False)
            if stock_report_type:
                # Search for especific picking type and report type
                domains.append([
                    ('stock_picking_type_ids', '=', record.picking_type_id.id),
                    ('stock_report_type', '=', stock_report_type),
                    ])
                # Search for especific report type
                domains.append([
                    ('stock_report_type', '=', stock_report_type),
                    ])
            # Search for especific picking type and report type
            domains.append([('stock_picking_type_ids', '=', record.picking_type_id.id)])
            # Search without picking_type
            domains.append([('stock_picking_type_ids', '=', False)])
            # Search without picking_type
            domains.append([('stock_report_type', '=', False)])
        return domains
