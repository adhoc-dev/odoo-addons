# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api


class SaleExceptionConfirm(models.TransientModel):

    _inherit = 'sale.exception.confirm'

    @api.one
    def action_confirm(self):
        res = super(SaleExceptionConfirm, self).action_confirm()
        if self.ignore:
            return self.sale_id.action_button_confirm()
        return res
