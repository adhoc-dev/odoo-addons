# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models
from openerp.osv import expression


class product_public_category(models.Model):
    _inherit = "product.public.category"

    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if not context:
            context = {}
        if name:
            # Be sure name_search is symetric to name_get
            categories = name.split('/')
            parents = list(categories)
            child = parents.pop()
            domain = [('name', operator, child)]
            if parents:
                names_ids = self.name_search(
                    cr, uid, '/'.join(parents), args=args, operator='ilike', context=context, limit=limit)
                category_ids = [name_id[0] for name_id in names_ids]
                if operator in expression.NEGATIVE_TERM_OPERATORS:
                    category_ids = self.search(
                        cr, uid, [('id', 'not in', category_ids)])
                    domain = expression.OR(
                        [[('parent_id', 'in', category_ids)], domain])
                else:
                    domain = expression.AND(
                        [[('parent_id', 'in', category_ids)], domain])
                for i in range(1, len(categories)):
                    domain = [
                        [('name', operator, '/'.join(categories[-1 - i:]))], domain]
                    if operator in expression.NEGATIVE_TERM_OPERATORS:
                        domain = expression.AND(domain)
                    else:
                        domain = expression.OR(domain)
            ids = self.search(
                cr, uid, expression.AND([domain, args]), limit=limit, context=context)
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
        return self.name_get(cr, uid, ids, context)

    def name_get(self, cr, uid, ids, context=None):
        res = []
        for cat in self.browse(cr, uid, ids, context=context):
            names = [cat.name]
            pcat = cat.parent_id
            while pcat:
                names.append(pcat.name)
                pcat = pcat.parent_id
            res.append((cat.id, '/'.join(reversed(names))))
        return res
