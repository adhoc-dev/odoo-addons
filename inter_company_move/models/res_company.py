# -*- coding: utf-8 -*-
from openerp.osv import osv, fields


class res_company(osv.osv):
    _inherit = 'res.company'

    _columns = {
        'invoice_move_type': fields.selection(
            [('not_available', 'Not Available'),
             ('move_wizard', 'Move With Wizard'),
             ('move_auto', 'Move Automatically')],
            string='Invoice Move Type', required=True),
        'open_after_move': fields.boolean(
            'Open New Record After Move?',
            help="Please note that to open the new record you must have the right access rights. This is only advisible when it is moved to a child company."),
        'deactivate_invoice': fields.boolean(
            'Deactivate Invoice'),
        'record_moved_id': fields.boolean(
            'Record Moved Id',
            help="Please note that to open the new record you must have the right access rights. This is only advisible when it is moved to a child company."),
        'invoice_move_company_id': fields.many2one('res.company',
                                                   'Destiny Company',),
    }

    _defaults = {
        'invoice_move_type': 'not_available',
    }
