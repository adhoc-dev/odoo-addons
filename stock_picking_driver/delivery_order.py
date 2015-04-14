from openerp import fields, models, _


class stock_picking(models.Model):

    _inherit = 'stock.picking'

    driver_id = fields.Many2one(
        'res.partner',
        'Driver')
