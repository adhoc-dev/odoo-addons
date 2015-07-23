# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, api, models, _


class stock_lot_ean128_report(models.TransientModel):

    _name = 'stock.lot.print_ean128_report'

    @api.model
    def _get_lot(self):
        active_id = self._context.get('active_id', False)
        return self.env['stock.production.lot'].browse(active_id)

    lot_id = fields.Many2one(
        'stock.production.lot', default=_get_lot)
    quantity = fields.Integer(string='Quantity', default=1)
    product_id = fields.Many2one(
        'product.product',
        related='lot_id.product_id',
        string="Product", readonly=True)

    @api.multi
    def do_print_report(self):

        self.ensure_one()
        return self.env['report'].get_action(
            self, 'report_stock_lot_EAN128')

    @api.multi
    def do_print_report_excel(self):

        self.ensure_one()
        return self.env['report'].get_action(
            self, 'report_stock_lot_EAN128_excel')


class stock_picking_ean128_report_detail(models.TransientModel):

    _name = 'stock.picking.print_ean128_report_detail'

    stock_picking_report_id = fields.Many2one(
        'stock.picking.print_ean128_report', 'Picking Report EAN Print')
    product_id = fields.Many2one(
        'product.product', string="Product", readonly=True)
    quantity = fields.Integer(string='Quantity')
    lot_id = fields.Many2one(
        'stock.production.lot', string='Lot', readonly=True)
    product_uom_id = fields.Many2one(
        'product.uom', string='UOM', readonly=True)


class stock_picking_ean128_report(models.TransientModel):
    _name = 'stock.picking.print_ean128_report'

    @api.model
    def _get_picking(self):
        active_id = self._context.get('active_id', False)
        return self.env['stock.picking'].browse(active_id)

    picking_id = fields.Many2one(
        'stock.picking',
        default=_get_picking
    )

    stock_picking_line_ids = fields.One2many(
        'stock.picking.print_ean128_report_detail',
        'stock_picking_report_id', 'Product Print'
    )

    @api.one
    @api.onchange('picking_id')
    def _compute_lines(self):
        self.stock_picking_line_ids = self.env[
            'stock.picking.print_ean128_report_detail']
        if self.picking_id.pack_operation_ids:
            lines = []
            for line in self.picking_id.pack_operation_ids:
                values = {
                    'product_id': line.product_id.id,
                    'quantity': line.product_qty,
                    'lot_id': line.lot_id.id,
                    'product_uom_id': line.product_uom_id.id,
                }
                lines.append((0, _, values))
            self.stock_picking_line_ids = lines

    @api.multi
    def do_print_report(self):

        self.ensure_one()
        return self.env['report'].get_action(
            self, 'report_stock_picking_EAN128')

    @api.multi
    def do_print_report_excel(self):

        self.ensure_one()
        return self.env['report'].get_action(
            self, 'report_stock_picking_EAN128_excel')
