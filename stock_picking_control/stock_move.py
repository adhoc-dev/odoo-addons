from openerp import models, api, fields, _
from openerp.exceptions import Warning


class stock_move_consume(models.TransientModel):

    _inherit = 'stock.transfer_details_items'

    @api.one
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

    location_type = fields.Selection(
        related='location_dest_id.usage', string='Location Type')
