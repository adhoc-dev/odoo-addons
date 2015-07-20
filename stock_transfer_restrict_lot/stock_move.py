from openerp import models, fields, api, _
from openerp.exceptions import Warning


class stock_transfer_details(models.TransientModel):

    _inherit = 'stock.transfer_details'

    code = fields.Selection(
        related='picking_id.picking_type_id.code',
        string='Operation Type')

    @api.one
    def do_detailed_transfer(self):
        super(stock_transfer_details, self).do_detailed_transfer()
        if self.code != 'incoming':
            item_lines = self.item_ids.read_group(
                [('id', 'in', self.item_ids.ids)],
                ['lot_id', 'quantity'], ['lot_id'])
            for item in item_lines:
                lot = self.env['stock.production.lot'].browse(
                    item['lot_id'][0])
                if lot:
                    quants = self.env['stock.quant'].search(
                        [('id', 'in', lot.quant_ids.ids),
                         ('location_id', '=', self.item_ids[0].sourceloc_id.id)])
                    if quants:
                        qty = sum([x.qty for x in quants])
                        if qty < item['quantity']:
                            raise Warning(
                                _('Sending amount can not exceed the quantity in stock for this product in this lot. \
                                \n Product:%s \
                                \n Lot:%s \
                                \n Stock:%s') % (lot.product_id.name, lot.name, qty))



class stock_transfer_details_items(models.TransientModel):

    _inherit = 'stock.transfer_details_items'

    code = fields.Selection(
        related='transfer_id.picking_id.picking_type_id.code',
        string='Operation Type')

    @api.one
    @api.constrains('lot_id')
    def _check_quantity_lot(self):
        obj_lot = self.env['stock.production.lot']
        lot_id = obj_lot.search([('id', '=', self.lot_id.id),
                                 ('product_id', '=', self.product_id.id)])
        if lot_id and self.code != 'incoming':
            quants = self.env['stock.quant'].search(
                [('id', 'in', lot_id.quant_ids.ids),
                 ('location_id', '=', self.sourceloc_id.id)])
            if quants:
                qty = sum([x.qty for x in quants])
                if qty < self.quantity:
                    raise Warning(
                        _('Sending amount can not exceed the quantity in stock for this product in this lot. \
                                \n Product:%s \
                                \n Lot:%s \
                                \n Stock:%s') % (self.product_id.name, self.lot_id.name, qty))
            else:
                raise Warning(
                    _('Sending amount can not exceed the quantity in stock for this product in this lot. \
                                \n Product:%s \
                                \n Lot:%s \
                                \n Stock:0') % (self.product_id.name, lot_id.name))
