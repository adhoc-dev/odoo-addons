# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models, api


class product(models.Model):

    """"""

    _inherit = 'product.product'

    internal_code = fields.Char(
        'Internal Code')

    def name_search(self, cr, uid, name, args=None,
                    operator='ilike', context=None, limit=100):
        args = args or []
        res = []
        if name:
            recs = self.search(
                cr, uid, [('internal_code', operator, name)] + args,
                limit=limit, context=context)
            res = self.name_get(cr, uid, recs)
        res += super(product, self).name_search(
            cr, uid,
            name=name, args=args, operator=operator, limit=limit)
        return res

    @api.model
    def create(self, vals):
        if (
                not vals.get('internal_code', False) and
                not self._context.get('default_internal_code', False)):
            vals['internal_code'] = self.env[
                'ir.sequence'].get('product.internal.code') or '/'
        return super(product, self).create(vals)

    _sql_constraints = {
        ('internal_code_uniq', 'unique(internal_code)',
            'Internal Code mast be unique!')
    }


class product_template(models.Model):

    """"""

    _inherit = 'product.template'

    internal_code = fields.Char(
        related='product_variant_ids.internal_code',
        string='Internal Code')

    @api.model
    def create(self, vals):
        if vals.get('internal_code'):
            self = self.with_context(
                default_internal_code=vals.get('internal_code'))
        return super(product_template, self).create(vals)
