# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models, api
from math import ceil


class stock_transfer_details(models.TransientModel):
    _inherit = 'stock.transfer_details'

    @api.model
    def _get_picking(self):
        active_id = self._context.get('active_id', False)
        return self.env['stock.picking'].browse(active_id)

    @api.model
    def _get_book(self):
        picking = self._get_picking()
        return picking.picking_type_id.book_id

    book_required = fields.Boolean(
        related='picking_id.picking_type_id.book_required'
        )
    book_id = fields.Many2one(
        'stock.book',
        'Book',
        default=_get_book,
        )
    # block_estimated_number_of_pages = fields.Boolean(
    #     related='book_id.block_estimated_number_of_pages',
    #     )
    next_voucher_number = fields.Integer(
        'Next Voucher Number',
        related='book_id.sequence_id.number_next_actual', readonly=True,
        )
    lines_per_voucher = fields.Integer(
        'Lines Per Voucher',
        related='book_id.lines_per_voucher',
        )

    @api.multi
    def get_estimated_number_of_pages(self):
        self.ensure_one()
        lines_per_voucher = self.lines_per_voucher
        if lines_per_voucher == 0:
            estimated_number_of_pages = 1
        else:
            operations = len(self.picking_id.pack_operation_ids)
            estimated_number_of_pages = int(ceil(
                float(operations) / float(lines_per_voucher)
                ))
        return estimated_number_of_pages

    @api.multi
    def do_detailed_transfer(self):
        self.ensure_one()
        super(stock_transfer_details, self).do_detailed_transfer()
        if self.book_required:
            self.picking_id.assign_numbers(
                self.get_estimated_number_of_pages(), self.book_id)
            return self.picking_id.do_print_voucher()
        return True
