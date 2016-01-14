# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api


class sale_order_line(models.Model):

    """"""

    _inherit = 'sale.order.line'

    @api.multi
    def product_id_change_with_wh(
            self, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False,
            fiscal_position=False, flag=False, warehouse_id=False):
        res = super(sale_order_line, self.with_context(
                preserve_uom=uom)).product_id_change_with_wh(
                pricelist, product, qty=qty, uom=uom,
                qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
                lang=lang, update_tax=update_tax, date_order=date_order,
                packaging=packaging, fiscal_position=fiscal_position,
                flag=flag, warehouse_id=warehouse_id)
        return res
