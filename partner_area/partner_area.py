# -*- coding: utf-8 -*-
##############################################################################
#
#    Ingenieria ADHOC - ADHOC SA
#    https://launchpad.net/~ingenieria-adhoc
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


import openerp
from openerp import SUPERUSER_ID
from openerp.osv import osv, fields
from openerp.tools.translate import _


class partner_area(osv.osv):
    _name = 'res.partner.area'
    _description = 'Area'
    
        
    _columns = {
        'name': fields.char( string='Name',required=True),
        }






class res_partner(osv.osv):
    _inherit = "res.partner"

    
        
    _columns = {
        'area_ids': fields.many2many('res.partner.area', string='Areas'),
        'parent_area_ids': fields.related('area_ids', 'parent_id', string='Parent Areas',type="one2many", relation="res.partner.area"),
        'area_id': fields.many2one('res.partner.area', string='Area'),
    }

   
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
