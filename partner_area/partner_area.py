# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _


class partner_area(osv.osv):
    _name = 'res.partner.area'
    _description = 'Area'
    _columns = {
        'name': fields.char(string='Name', required=True),
    }

    def create(self, cr, uid, vals, context=None):
        if 'from_m2m' not in context:
            raise osv.except_osv(
                _('Warning!'), _('You can only create Areas from companies!'))
        return super(partner_area, self).create(cr, uid, vals, context=context)


class res_partner(osv.osv):
    _inherit = "res.partner"

    _columns = {
        'area_ids': fields.many2many(
            'res.partner.area', string='Areas'),
        'parent_area_ids': fields.related(
            'parent_id', 'area_ids', string='Parent Areas',
            type="many2many", relation="res.partner.area"),
        'area_id': fields.many2one('res.partner.area', string='Area'),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
