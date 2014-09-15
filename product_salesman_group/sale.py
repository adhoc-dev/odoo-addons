# -*- coding: utf-8 -*-
from openerp.osv import fields, osv


class salesman_group(osv.osv):

    _name = "sale.salesman.group"
    _description = "Salesman Group"
    _order = "name"

    _constraints = [
        (osv.osv._check_recursion,
         'Error ! You cannot create recursive categories.', ['parent_id'])
    ]

    def name_get(self, cr, uid, ids, context=None):
        if not len(ids):
            return []
        reads = self.read(cr, uid, ids, ['name', 'parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1] + ' / ' + name
            res.append((record['id'], name))
        return res

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)

    _columns = {
        'name': fields.char('Name', required=True, translate=True),
        'complete_name': fields.function(
            _name_get_fnc, type="char", string='Name'),
        'parent_id': fields.many2one(
            'sale.salesman.group', 'Parent Group', select=True),
        'child_id': fields.one2many(
            'sale.salesman.group', 'parent_id', string='Children Groups'),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
