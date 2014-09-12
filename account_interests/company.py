# -*- coding: utf-8 -*-
from openerp.osv import osv, fields


class company(osv.osv):

    """"""

    _inherit = 'res.company'

    _columns = {
        'debt_interest_period': fields.integer(string='Debt Interest Months', help="Create interest for debt greater than x months")
    }
    _defaults = {
        'debt_interest_period': 1,
    }