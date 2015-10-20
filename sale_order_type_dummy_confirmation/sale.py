# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import api, models


class sale_order(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def get_use_dummy_confirm(self):
        self.ensure_one()
        dummy_confirm = super(sale_order, self).get_use_dummy_confirm()
        if not dummy_confirm:
            dummy_confirm = self.type_id.dummy_confirm
        return dummy_confirm
