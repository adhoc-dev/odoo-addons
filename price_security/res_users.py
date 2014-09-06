# -*- coding: utf-8 -*-
from openerp import models, api, fields, _


class discount_restriction(models.Model):
    _name = 'price_security.discount_restriction'
    _description = 'Discount Restriction'

    name = fields.Char(
        'Name',
        required=True)
    pricelist_id = fields.Many2one(
        'product.pricelist',
        'Pricelist')
    min_discount = fields.Float('Min. Discount')
    max_discount = fields.Float('Max. Discount')
    user_id = fields.Many2one(
        'res.users',
        'User',
        required=True)

    @api.multi
    def check_discount_with_restriction(self, discount, pricelist_id):
        return True
        # restriction_id = self.get_restriction_id(
        #     cr, uid, uid, pricelist_id, context=context)

        # group_obj = self.pool.get('res.groups')
        # if not group_obj.user_in_group(cr, uid, uid, 'price_security.can_modify_prices', context=context):
        #     titulo = _('Discount out of range')
        #     mensaje_1 = _(
        #         'The applied discount is out of range with respect to the allowed. The discount can be between %s and %s for the current price list.')
        #     mensaje_2 = _(
        #         'The applied discount is out of range with respect to the allowed. You cannot give any discount with the current price list.')

        #     if restriction_id:
        #         restriction = self.browse(
        #             cr, uid, restriction_id, context=context)
        #         if isinstance(restriction, list):
        #             restriction = restriction[0]
        #         if discount < restriction.min_discount or discount > restriction.max_discount:
        #             raise osv.except_osv(
        # titulo, mensaje_1 % (restriction.min_discount,
        # restriction.max_discount))

        #     elif discount > 0:
        #         raise osv.except_osv(titulo, mensaje_2)

    @api.multi
    def get_restriction_id(self, user_id, pricelist_id):
        return True
        # filters = [('user_id', '=', user_id)]
        # if pricelist_id:
        #     filters.append(('pricelist_id', '=', pricelist_id))
        # restriction_id = self.search(cr, uid, filters, context=context)

        # if not restriction_id:
        #     filters = [('user_id', '=', user_id), ('pricelist_id', '=', False)]
        #     restriction_id = self.search(cr, uid, filters, context=context)

        # if not restriction_id:
        #     return False

        # if isinstance(restriction_id, list):
        #     restriction_id = restriction_id[0]
        # return restriction_id


class users(models.Model):
    _inherit = 'res.users'

    restrict_prices = fields.Boolean(
        'Restrict Prices for this User?')
    discount_restriction_ids = fields.One2many(
        'price_security.discount_restriction',
        'user_id',
        string='Discount Restrictions')
