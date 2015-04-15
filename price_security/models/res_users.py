# -*- coding: utf-8 -*-
from openerp import models, api, fields, _
from openerp.exceptions import Warning


class discount_restriction(models.Model):
    _name = 'res.users.discount_restriction'
    _description = 'Discount Restriction'

    pricelist_id = fields.Many2one(
        'product.pricelist',
        'Pricelist',
        ondelete='cascade',)
    min_discount = fields.Float('Min. Discount', required=True)
    max_discount = fields.Float('Max. Discount', required=True)
    user_id = fields.Many2one(
        'res.users',
        'User',
        required=True,
        ondelete='cascade',
        )


class users(models.Model):
    _inherit = 'res.users'

    discount_restriction_ids = fields.One2many(
        'res.users.discount_restriction',
        'user_id',
        string='Discount Restrictions')

    @api.multi
    def check_discount(self, discount, pricelist_id):
        if discount and discount != 0.0:
            disc_restriction_env = self.env['res.users.discount_restriction']
            domain = [
                ('pricelist_id', '=', pricelist_id), ('user_id', '=', self.id)]
            disc_restrictions = disc_restriction_env.search(domain)
            if not disc_restrictions.ids:
                domain = [
                    ('user_id', '=', self.id)]
                disc_restrictions = disc_restriction_env.search(domain)
                # User can not make any discount
                if not disc_restrictions.ids:
                    raise Warning(_('You can not give any discount greater than pricelist discounts'))
            disc_restriction = disc_restrictions[0]
            if discount < disc_restriction.min_discount or discount > disc_restriction.max_discount:
                    raise Warning(_('The applied discount is out of range with respect to the allowed. The discount can be between %s and %s for the current price list') % (disc_restriction.min_discount, disc_restriction.max_discount))
        return True
