# -*- coding: utf-8 -*-
from openerp import models, fields
import openerp.addons.decimal_precision as dp


class res_partner_sample(models.Model):
    _name = "res.partner.sample"
    _description = "Partner Samples"
    _order = 'delivery_date desc'

    delivery_date = fields.Date(
        string='Delivery Date',
        required=True,
        default=fields.Date.context_today)
    user_id = fields.Many2one(
        'res.users',
        required=True,
        default=lambda self: self.env.user,
        string='User',)
    partner_id = fields.Many2one(
        'res.partner',
        required=True,
        string='Partner')
    product_id = fields.Many2one(
        'product.product',
        required=True,
        string='Product')
    quantity = fields.Float(
        'Quantity',
        required=True,
        digits_compute=dp.get_precision('Product UoS'))
    return_date = fields.Date(
        string='Return Date',)


class res_partner(models.Model):
    _inherit = "res.partner"

    sample_ids = fields.One2many(
        'res.partner.sample',
        'partner_id',
        'Samples')
