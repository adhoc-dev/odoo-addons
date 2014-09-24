# -*- coding: utf-8 -*-
from openerp import models, fields


class ir_actions_report(models.Model):
    _inherit = 'ir.actions.report.xml'

    stock_picking_type_ids = fields.Many2many(
        'stock.picking.type',
        'report_configuration_stock_picking_type_rel',
        'report_configuration_id', 'picking_type_id', 'Picking Types')
    stock_picking_split_picking_type_out = fields.Boolean(
        'Split Out Picking',
        help="Split picking if type operation is 'Out'.")
    stock_picking_split_picking_type_in = fields.Boolean(
        'Split In Picking',
        help="Split picking if type operation is 'In'.")
    stock_picking_split_picking_type_internal = fields.Boolean(
        'Split Internal Picking',
        help="Split picking if type operation is 'Internal'.")
    stock_picking_lines_to_split = fields.Integer(
        'Lines to split')
    stock_picking_dont_split_option = fields.Boolean(
        'Dont Split Option',
        help="Add a 'Don't Split' option on picking that should be splitted.")
    stock_report_type = fields.Selection(
        [('remit', 'Remit'), ('picking_list', 'Picking List')],
        'Stock Report Type',)

    def get_domains(self, cr, model, record, context=None):
        domains = super(ir_actions_report, self).get_domains(
            cr, model, record, context=context)
        if model == 'stock.picking':
            stock_report_type = context.get('stock_report_type', False)
            print 'stock_report_type', stock_report_type
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
