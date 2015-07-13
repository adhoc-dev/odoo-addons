from openerp import models, api, _
from openerp.exceptions import Warning


class stock_move_consume(models.TransientModel):

    _inherit = 'stock.transfer_details_items'

    @api.one
    @api.constrains('lot_id')
    def _check_quantity_lot(self):
        obj_lot = self.env['stock.production.lot']
        obj_quant = self.env['stock.quant']
        lot_id = obj_lot.search([('id', '=', self.lot_id.id),
                                 ('product_id', '=', self.product_id.id)])
        if lot_id:
            quants = obj_quant.search(
                [('id', 'in', lot_id.quant_ids.ids),
                 ('location_id', '=', self.sourceloc_id.id)])
            if quants:
                qty = sum([x.qty for x in quants])
                if qty < self.quantity:
                    raise Warning(
                        _('Sending amount can not exceed the quantity in stock for this lot. %s Stock Units') % (qty))
            else:
                raise Warning(
                    _('No stock of this product on this lot %s') % (lot_id.name))
