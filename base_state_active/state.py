# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################


from openerp.osv import osv
from openerp.osv import fields

class res_country_state(osv.osv):
    _inherit = 'res.country.state'

    _columns = {
        'active':fields.boolean('Active',),
    }
    
    _defaults = {
    	'active':True,
    }