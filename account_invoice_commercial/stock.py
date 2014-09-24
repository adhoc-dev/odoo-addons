# -*- coding: utf-8 -*-
from openerp import models


class stock_picking(models.Model):
    _inherit = "stock.picking"

#TODO migrate this to odoo v8
    # def _prepare_invoice(self, cr, uid, picking, partner, inv_type, journal_id, context=None):
    #     ret = super(stock_picking, self)._prepare_invoice(cr, uid, picking, partner, inv_type, journal_id, context=context)

    #     if not ret.has_key('value'):
    #         ret['value'] = {}

    #     ret['user_id'] = partner.user_id.id or uid
            
    #     return ret
