# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import netsvc
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _

class res_partner_source(osv.osv):
    _name = "res.partner.source"
    _description = "Partner Source"
    _order = "name"

    _columns = {
        'name': fields.char('Name', required=True, translate=True),
    }


class res_partner(osv.osv):
    _inherit = "res.partner"

    _columns = {
    	'source_id': fields.many2one('res.partner.source', string='Source',),
    }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
