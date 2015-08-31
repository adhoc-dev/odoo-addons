# -*- coding: utf-8 -*-
from openerp.osv import fields, osv


class crm_phonecall_type(osv.osv):
    _name = "crm.phonecall.type"
    _description = "Phonecall Types"
    # _order = "name"
    _columns = {
        'name': fields.char('Name', required=True),
    }


class crm_phonecall(osv.osv):
    _inherit = "crm.phonecall"

    _columns = {
        'type_id': fields.many2one(
            'crm.phonecall.type',
            'Type',),
    }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
