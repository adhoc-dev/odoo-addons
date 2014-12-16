# -*- coding: utf-8 -*-
from openerp.osv import osv, fields


class crm_lead(osv.osv):
    _inherit = "crm.lead"

    _columns = {
        'area_id': fields.many2one('res.partner.area', string='Area'),
    }

    def onchange_partner_id(self, cr, uid, ids, partner_id, context=None):
        result = super(crm_lead, self).onchange_partner_id(
            cr, uid, ids, partner_id)
        if partner_id:
            partner = self.pool['res.partner'].browse(
                cr, uid, partner_id, context=context)
            result['value'].update({
                'area_id': partner.area_id and partner.area_id.id or False, })
        return result

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
