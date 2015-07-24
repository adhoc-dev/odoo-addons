# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import netsvc
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

def location_name_search(self, cr, user, name='', args=None, operator='ilike',
                         context=None, limit=100):
    if not args:
        args = []

    ids = []
    if len(name) == 2:
        ids = self.search(cr, user, [('code', 'ilike', name)] + args,
                          limit=limit, context=context)

    search_domain = [('name', operator, name)]
    if ids: search_domain.append(('id', 'not in', ids))
    ids.extend(self.search(cr, user, search_domain + args,
                           limit=limit, context=context))

    locations = self.name_get(cr, user, ids, context)
    return sorted(locations, key=lambda (id, name): ids.index(id))

class res_partner_establishment_activity(osv.osv):
    _name = "res.partner.establishment.activity"
    _description = "Establishment Activity"
    _columns = {
        'name': fields.char('Name', required=True, translate=True),    
        }

class res_partner_establishment_tenure(osv.osv):
    _name = "res.partner.establishment.tenure"
    _description = "Establishment Tenure"
    _columns = {
        'name': fields.char('Name', required=True, translate=True),    
        }

class StateDepartment(osv.osv):
    _description="State department"
    _name = 'res.country.state.department'
    _columns = {
        'state_id': fields.many2one('res.country.state', 'State',
            required=True),
        'name': fields.char('Department Name', size=64, required=True, 
                            help='Administrative divisions of a state.'),
    }
    _order = 'name'

    name_search = location_name_search

class res_partner_establishment(osv.osv):
    _name = "res.partner.establishment"
    _description = "Partner Establishment"
    _order = "name"

    _columns = {
        'name': fields.char('Name', required=True, translate=True),
        'street': fields.char('Street', size=128),
        'street2': fields.char('Street2', size=128),
        'department_id': fields.many2one("res.country.state.department", 'Department'),
        'zip': fields.char('Zip', change_default=True, size=24),
        'city': fields.char('City', size=128),
        'state_id': fields.many2one("res.country.state", 'State', required=True, ),
        'country_id': fields.many2one('res.country', 'Country', required=True, ),
        'note': fields.text('Notes'),
        'surface': fields.float('Surface', required=True, digits_compute=dp.get_precision('Establishment Surface')),
        'surface_uom_id': fields.many2one('product.uom', 'Unit of Measure', required=True, readonly=False, help="Unit of measurement for Surface",),
        'tenure_id': fields.many2one('res.partner.establishment.tenure', 'Tenure'),
        'partner_id': fields.many2one('res.partner', 'Partner', required=True, ondelete='cascade', domain=[('is_company','=',True)], context={'default_is_company':True},),
        'activity_ids': fields.many2many('res.partner.establishment.activity', rel='res_establishment_activity_rel', id1='establishment_id', id2='partner_id', string='Activities'),
        # 'activity_id': fields.many2one('res.partner.establishment.activity', 'Activity'),
    }

    def onchange_state(self, cr, uid, ids, state_id, context=None):
        if state_id:
            country_id = self.pool.get('res.country.state').browse(cr, uid, state_id, context).country_id.id
            return {'value':{'country_id':country_id}}
        return {}    

class res_partner(osv.osv):
    _inherit = "res.partner"

    _columns = {
        'establishment_ids': fields.one2many('res.partner.establishment', 'partner_id', string='Establishments',),
    	# 'establishment_ids': fields.many2one('res.partner.establishment', string='Establishments',),
    }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
