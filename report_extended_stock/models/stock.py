# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api


class stock_picking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def do_print_picking(self):
        '''This function prints the picking list'''
        assert len(
            self) == 1, 'This option should only be used for a single id at a time.'
        report_obj = self.env['ir.actions.report.xml']
        report_name = report_obj.with_context(
            stock_report_type='picking_list').get_report_name(
            'stock.picking', self.ids)
        return self.env['report'].get_action(self, report_name)

    @api.multi
    def do_print_voucher(self):
        '''This function prints the voucher'''
        assert len(
            self) == 1, 'This option should only be used for a single id at a time.'
        report_obj = self.env['ir.actions.report.xml']
        report_name = report_obj.with_context(
            stock_report_type='voucher').get_report_name(
            'stock.picking', self.ids)
        report = self.env['report'].get_action(self, report_name)
        if self._context.get('keep_wizard_open', False):
            report['type'] = 'ir.actions.report_dont_close_xml'
        return report

    @api.model
    def _get_invoice_vals(self, key, inv_type, journal_id, move):
        vals = super(stock_picking, self)._get_invoice_vals(
            key, inv_type, journal_id, move)
        if 'comment' in vals:
            vals.pop('comment')
        vals.update({
            'internal_notes': move.picking_id.note})
        return vals


class stock_move(models.Model):
    _inherit = 'stock.move'

    @api.model
    def _prepare_picking_assign(self, move):
        res = super(stock_move, self)._prepare_picking_assign(move)
        res.update({
            'note': move.procurement_id.sale_line_id.order_id.internal_notes})
        return res
