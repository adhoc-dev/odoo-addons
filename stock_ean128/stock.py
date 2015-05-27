# -*- coding: utf-8 -*-
from openerp import models, fields, api


class stock_picking(models.Model):
    _inherit = 'stock.production.lot'

    ean_128 = fields.Char(string="EAN128")

    @api.one
    def action_compute(self):
        name = ''
        if self.product_id.default_code:
            name += '(01)' + self.product_id.default_code
        name += '(10)' + self.name
        if self.life_date:
            life_date = fields.Datetime.from_string(self.life_date)
            name += '(17)' + life_date.strftime('%d%m%y')
        else:
            name += '(17)' + 'N/A'
        self.ean_128 = name
