# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class sale_global_discount_wizard(models.TransientModel):
    _name = "sale.order.global_discount.wizard"

    # todo implement fixed amount
    # type = fields.Selection([
    #     ('percentage', 'Percentage'),
    #     ('fixed_amount', 'Fixed Amount'),
    #     ],
    #     'Type',
    #     required=True,
    #     default='percentage',
    #     )
    amount = fields.Float(
        # 'Amount',
        'Discount',
        required=True,
        )

    @api.multi
    def confirm(self):
        self.ensure_one()
        order = self.env['sale.order'].browse(
            self._context.get('active_id', False))
        for line in order.order_line:
            line.discount = self.amount
        return True
