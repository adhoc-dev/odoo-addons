# -*- coding: utf-8 -*-
from openerp import models, fields


class stock_picking(models.Model):
    _inherit = 'stock.picking'

    observations = fields.Text('Observations')

    def do_print_picking(self, cr, uid, ids, context=None):
        '''This function prints the picking list'''
        context = context or {}
        context['active_ids'] = ids
        report_obj = self.pool.get('ir.actions.report.xml')
        report_name = report_obj.get_report_name(
            cr, uid, 'stock.picking', ids, context=context)

        return self.pool.get("report").get_action(
            cr, uid, ids, report_name, context=context)
