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

from osv import osv
from osv import fields

class groups(osv.osv):
    _name = 'res.groups'
    _inherit = 'res.groups'
    
    def id_from_xml_id(self, cr, uid, xml_id, context=None):
        group_obj = self.pool.get('res.groups')
        group_all_ids = group_obj.search(cr, uid, [], context=context)
        group_xml_ids = group_obj.get_xml_id(cr, uid, group_all_ids, context=context)
        
        for key in group_xml_ids.keys():
            xml_id_it = group_xml_ids[key]
            if xml_id_it == xml_id:
                return key
        return False
        
    def user_in_group(self, cr, uid, user_id, group_xml_id, context=None):
        user_obj = self.pool.get('res.users')
        user = user_obj.browse(cr, uid, user_id, context=context)
        if isinstance(user, list):
            user = user[0]
        
        group_id = self.id_from_xml_id(cr, uid, group_xml_id, context=context)
        for group in user.groups_id:
            if group.id == group_id:
                return True
        return False

groups()

