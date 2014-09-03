# -*- coding: utf-8 -*-
from osv import osv, fields
import netsvc


class stock_picking(osv.osv):

    _inherit = 'stock.picking'
