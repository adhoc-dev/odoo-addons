# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api


class products_to_quotation_wizard(models.TransientModel):
    _name = 'sale.products_to_quotation_wizard'

    @api.model
    def _get_quotation(self):
        quotation = self.env['sale.order'].search(
            [('state', '=', 'draft'),
             ('write_uid', '=', self._uid)], limit=1)
        return quotation

    quotation = fields.Many2one(
        'sale.order',
        domain=[('state', '=', 'draft')],
        default=_get_quotation
    )

    @api.one
    def add_to_quotation(self):
        active_ids = self._context['active_ids']
        self.quotation.add_products(active_ids)
