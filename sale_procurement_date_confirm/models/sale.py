# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class sale_order(models.Model):
    _inherit = "sale.order"

    @api.model
    def _prepare_order_line_procurement(self, order, line, group_id=False):
        res = super(sale_order, self)._prepare_order_line_procurement(
            order, line, group_id=group_id)
        # because _get_date_planned receive a datetime string, we convert it
        date_confirm = fields.Datetime.to_string(
            fields.Datetime.from_string(order.date_confirm))
        res['date_planned'] = self._get_date_planned(
            order, line, date_confirm)
        return res
