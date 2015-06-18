# -*- coding: utf-8 -*-
from openerp import models, fields, api


class stock_production_lot(models.Model):
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

    def name_search(
            self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        res = super(stock_production_lot, self).name_search(
            cr, uid, name=name, args=args, operator=operator, context=context, limit=limit)
        ids = self.search(cr, uid, [('ean_128', operator, name)],
                          limit=limit, context=context)
        res += self.name_get(cr, uid, ids, context=context)
        return res
