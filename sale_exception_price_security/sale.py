# -*- coding: utf-8 -*-
from openerp import models, api


class sale_order_line(models.Model):
    _inherit = "sale.order.line"

    @api.one
    def check_discount(self):
        # disable price_security constraint
        return True

    @api.multi
    def check_discount_ok(self):
        self.ensure_one()
        # disable constrant
        if (
                self.user_has_groups('price_security.group_restrict_prices')
                and not self.product_can_modify_prices
                ):
            # if something, then we have an error, not ok
            if self.env.user.check_discount(
                    self.discount,
                    self.order_id.pricelist_id.id,
                    do_not_raise=True):
                return False
        return True
