from openerp import models, api, fields, _
from openerp.exceptions import Warning


class stock_transfer_details(models.TransientModel):

    _inherit = 'stock.transfer_details'

    block_quantity = fields.Boolean(
        related='picking_id.block_quantity')

    @api.one
    @api.constrains('item_ids')
    def _check_quantity(self):
        if self.item_ids and self.block_quantity:
            for move in self.picking_id.move_lines:
                qty = 0.0
                for item in self.env['stock.transfer_details_items'].search(
                    [('id', 'in', self.item_ids.ids),
                     ('product_id', '=', move.product_id.id)]):
                    qty = qty + item.quantity
                if qty > move.product_qty:
                    raise Warning(
                        _('Quantity to send for "%s" can not be greater than the remaining quantity for this move.') % (move.product_id.name))


class stock_move(models.Model):

    _inherit = 'stock.move'

    block_quantity = fields.Boolean(
        related='picking_id.block_quantity')


class stock_picking(models.Model):

    _inherit = 'stock.picking'

    block_quantity = fields.Boolean(compute='_get_block_quantity')

    @api.one
    @api.depends(
        'picking_type_id.code',
        'company_id.block_internal_move',
        'company_id.block_outgoing_move',
        'company_id.block_incoming_move'
    )
    def _get_block_quantity(self):
        self.block_quantity = False
        if self.company_id.block_internal_move and self.picking_type_id.code == 'internal':
            self.block_quantity = True
        elif self.company_id.block_outgoing_move and self.picking_type_id.code == 'outgoing':
            self.block_quantity = True
        elif self.company_id.block_incoming_move and self.picking_type_id.code == 'incoming':
            self.block_quantity = True
