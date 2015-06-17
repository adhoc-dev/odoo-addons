# -*- coding: utf-8 -*-
from openerp import models


class stock_production_lot(models.Model):
    _inherit = 'stock.production.lot'

    def name_search(
            self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        res = super(stock_production_lot, self).name_search(
            cr, uid, name=name, args=args, operator=operator, context=context, limit=limit)
        ids = self.search(cr, uid, [('ean_128', operator, name)],
                          limit=limit, context=context)
        res += self.name_get(cr, uid, ids, context=context)
        return res
