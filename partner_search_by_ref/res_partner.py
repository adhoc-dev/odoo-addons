# -*- encoding: utf-8 -*-
from openerp import models
import re


class res_partner(models.Model):

    _inherit = 'res.partner'

    def name_search(self, cr, user, name, args=None, operator='ilike',
                    context=None, limit=100):
        if not args:
            args = []
        if context is None:
            context = {}
        ids = []
        if name:
            ptrn_name = re.compile('(\[(.*?)\])')
            res_name = ptrn_name.search(name)
            if res_name:
                name = name.replace('[' + res_name.group(2) + '] ', '')
            partner_search = super(res_partner, self).name_search(cr, user,
                                                                  name, args, operator, context, limit)
            ids = [partner[0] for partner in partner_search]
            if not ids:
                ids = self.search(cr, user, [('ref', operator, name)] + args,
                                  limit=limit, context=context)
            # if not ids:
            #     ptrn = re.compile('(\[(.*?)\])')
            #     res = ptrn.search(name)
            #     if res:
            #         ids = self.search(cr, user,
            #                           [('vat', operator, res.group(2))] + args, limit=limit,
            #                           context=context)
        else:
            return super(res_partner, self).name_search(cr, user,
                                                        name, args, operator, context, limit)

        return self.name_get(cr, user, ids, context=context)