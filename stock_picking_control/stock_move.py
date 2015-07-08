from openerp import models, api, fields, _
from openerp.exceptions import Warning


class stock_transfer_details(models.TransientModel):

    _inherit = 'stock.transfer_details'

    @api.one
    @api.constrains('item_ids')
    def _check_quantity(self):
        obj_move = self.env['stock.move']
        moves = self.picking_id.move_lines
        move = obj_move.browse(moves[0].id)
        if self.item_ids:
            qty = 0.0
            for item in self.item_ids:
                qty = qty + item.quantity
            if qty > move.product_qty:
                raise Warning(
                    _('Quantity to send can not be greater than the remaining quantity for this move.'))


class stock_move_consume(models.TransientModel):

    _inherit = 'stock.transfer_details_items'

    @api.constrains('quantity')
    def _check_quantity(self):
        obj_move = self.env['stock.move']
        moves = self.transfer_id.picking_id.move_lines
        move = obj_move.browse(moves[0].id)
        if move.product_qty < self.quantity:
            raise Warning(
                _('Quantity to send can not be greater than the remaining quantity for this move.'))


class stock_move(models.Model):

    _inherit = 'stock.move'

    code = fields.Selection(
        related='picking_type_id.code', string='Operation Type')


class stock_picking(models.Model):

    _inherit = 'stock.picking'

    code = fields.Selection(
        related='picking_type_id.code', string='Operation Type')
