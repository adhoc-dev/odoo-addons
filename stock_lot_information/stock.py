from openerp import models, fields


class stock_production_lot(models.Model):

    _inherit = 'stock.production.lot'

    ref_initial = fields.Integer(string='Initial reference')
    ref_final = fields.Integer(string='Final reference')
