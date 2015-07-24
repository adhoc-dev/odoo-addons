# -*- coding: utf-8 -*-


from openerp import models, fields


class company(models.TransientModel):

    _inherit = 'res.company'

    block_internal_move = fields.Boolean(
        string="Internal",
        help="Restrict the quantities in the Internal moves")
    block_outgoing_move = fields.Boolean(
        string="Outgoing",
        help="Restrict the quantities in the Outgoing moves")
    block_incoming_move = fields.Boolean(
        string="Incoming",
        help="Restrict the quantities in the Incoming moves")
