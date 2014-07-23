# -*- coding: utf-8 -*-
from openerp.tools.translate import _
from openerp.osv import fields, osv

class meeting(osv.osv):
    _name = "crm.meeting"
    _inherit = ["crm.meeting",'pad.common']
    _columns = {
        'description_pad': fields.char('Description PAD', pad_content_field='description')
    }
