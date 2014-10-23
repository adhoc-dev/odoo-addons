# -*- coding: utf-8 -*-
from openerp import models, fields, api, SUPERUSER_ID


class product_attribute(models.Model):
    _inherit = "product.attribute"
    add_to_name = fields.Boolean('Add To Name?', default=True)


class product_product(models.Model):
    _inherit = 'product.product'

    @api.one
    @api.depends(
        'product_tmpl_id',
        'product_tmpl_id.name',
        'attribute_value_ids',
        'attribute_value_ids.attribute_id',
        'attribute_value_ids.attribute_id.add_to_name',
        'attribute_line_ids',
        'attribute_line_ids.attribute_id.add_to_name',
        'attribute_line_ids.value_ids',
        'attribute_line_ids.value_ids.name',
    )
    def _get_complete_name(self):
        name = self.product_tmpl_id.name
        variants = [
            v.name for v in self.attribute_value_ids if v.attribute_id.add_to_name]
        attribute_lines = [
            v for v in self.attribute_line_ids if v.attribute_id.add_to_name and len(v.value_ids) == 1]
        attributes = [
            v.value_ids[0].name for v in attribute_lines if v.value_ids]
        variant_and_attributes = ", ".join(variants + attributes)
        name = variant_and_attributes and "%s (%s)" % (
            name, variant_and_attributes) or name
        self.name = name

    name = fields.Char(
        'Complete Name',
        compute='_get_complete_name',
        store=True,
    )

# Overwrite of name_get function to avoid joining variants again
    def name_get(self, cr, user, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        if not len(ids):
            return []

        def _name_get(d):
            name = d.get('name', '')
            code = context.get('display_default_code', True) and d.get(
                'default_code', False) or False
            if code:
                name = '[%s] %s' % (code, name)
            return (d['id'], name)

        partner_id = context.get('partner_id', False)
        if partner_id:
            partner_ids = [partner_id, self.pool['res.partner'].browse(
                cr, user, partner_id, context=context).commercial_partner_id.id]
        else:
            partner_ids = []

        # all user don't have access to seller and partner
        # check access and use superuser
        self.check_access_rights(cr, user, "read")
        self.check_access_rule(cr, user, ids, "read", context=context)

        result = []
        for product in self.browse(cr, SUPERUSER_ID, ids, context=context):
            # variant = ", ".join([v.name for v in product.attribute_value_ids])
            # name = variant and "%s (%s)" % (product.name, variant) or product.name
            name = product.name
            sellers = []
            if partner_ids:
                sellers = filter(
                    lambda x: x.name.id in partner_ids, product.seller_ids)
            if sellers:
                for s in sellers:
                    seller_variant = s.product_name and "%s (%s)" % (
                        s.product_name, variant) or False
                    mydict = {
                        'id': product.id,
                        'name': seller_variant or name,
                        'default_code': s.product_code or product.default_code,
                    }
                    result.append(_name_get(mydict))
            else:
                mydict = {
                    'id': product.id,
                    'name': name,
                    'default_code': product.default_code,
                }
                result.append(_name_get(mydict))
        return result
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
# Name search modificada para que busque tambien por los atributos
    # def name_search(self, cr, user, name='', args=None, operator='ilike', context=None, limit=100):
    #     if not args:
    #         args = []
    #     if name:
    #         positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
    #         ids = []
    #         if operator in positive_operators:
    #             ids = self.search(cr, user, [('default_code','=',name)]+ args, limit=limit, context=context)
    #             if not ids:
    #                 ids = self.search(cr, user, [('ean13','=',name)]+ args, limit=limit, context=context)
    #         if not ids and operator not in expression.NEGATIVE_TERM_OPERATORS:
    # Do not merge the 2 next lines into one single search, SQL search performance would be abysmal
    # on a database with thousands of matching products, due to the huge merge+unique needed for the
    # OR operator (and given the fact that the 'name' lookup results come from the ir.translation table
    # Performing a quick memory merge of ids in Python will give much better performance
    #             ids = set(self.search(cr, user, args + [('default_code', operator, name)], limit=limit, context=context))
    #             if not limit or len(ids) < limit:
    # we may underrun the limit because of dupes in the results, that's fine
    #                 limit2 = (limit - len(ids)) if limit else False
    #                 ids.update(self.search(cr, user, args + [('name', operator, name)], limit=limit2, context=context))
    # ESTO LO AGREGAMOS
    #             if not limit or len(ids) < limit:
    #                 print '11111'
    #                 limit3 = (limit - len(ids)) if limit else False
    #                 ids.update(self.search(cr, user, args + [('attribute_value_ids', operator, name)], limit=limit3, context=context))
    #             ids = list(ids)
    #         elif not ids and operator in expression.NEGATIVE_TERM_OPERATORS:
    #             ids = self.search(cr, user, args + ['&', ('default_code', operator, name), ('name', operator, name)], limit=limit, context=context)
    #         if not ids and operator in positive_operators:
    #             ptrn = re.compile('(\[(.*?)\])')
    #             res = ptrn.search(name)
    #             if res:
    #                 ids = self.search(cr, user, [('default_code','=', res.group(2))] + args, limit=limit, context=context)
    #     else:
    #         ids = self.search(cr, user, args, limit=limit, context=context)
    #     result = self.name_get(cr, user, ids, context=context)
    #     return result
