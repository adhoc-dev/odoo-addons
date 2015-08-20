# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api


class purchase_order(models.Model):
    _inherit = 'purchase.order'

    @api.one
    def update_prices(self):
        for line in self.order_line:
            price = self.pricelist_id.price_get(
                line.product_id.id,
                line.product_qty or 1.0,
                self.partner_id.id, context={
                    'uom': line.product_uom.id,
                    'date': self.date_order,
                })[self.pricelist_id.id]
            line.write({'price_unit': price})
        return True
