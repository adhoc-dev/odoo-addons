# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api, _
from openerp.exceptions import Warning
from datetime import datetime


class product_product(models.Model):
    _inherit = "product.product"

    @api.model
    def search_last_quotation(self):
        now = datetime.today()
        minute = now.minute - 5
        if minute < 0:
            minute = 60 - minute
        last_update = now.replace(
            minute=minute).strftime("%Y-%m-%d %H:%M:%S")
        quotation = self.env['sale.order'].search(
            [('state', '=', 'draft'),
             ('write_uid', '=', self._uid),
             ('write_date', '>=', last_update)], limit=1)
        if not quotation:
            raise Warning(_(
                'Do not found quotation modified by the user "%s" in the past '
                '5 minutes') % (
                self.env.user.name))
        return quotation

    @api.multi
    def add_to_last_quotation_button(self):
        quotation = self.search_last_quotation()
        quotation.add_products(self.id)

    def add_to_last_quotation(self, cr, uid, actives):
        quotation = self.search_last_quotation(cr, uid)
        quotation.add_products(actives)
