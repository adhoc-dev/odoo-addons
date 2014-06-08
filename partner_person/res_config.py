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

from openerp.osv import fields, osv
from openerp.tools.translate import _

class partner_configuration(osv.osv_memory):
    _name = 'partner.config.settings'
    _inherit = 'res.config.settings'

    _columns = {
        'group_disabilities': fields.boolean("Show Disabilities Information",
            implied_group='partner_person.person_disabilities',
            help="Show Disabilities Information Tab"),
        'group_person_ni': fields.boolean("Show National Identity",
            implied_group='partner_person.person_ni',
            help="Show National Identity Field in Personal Information Tab"),
        'group_person_passport': fields.boolean("Show Passport",
            implied_group='partner_person.person_passport',
            help="Show Passport Field in Personal Information Tab"),
        'group_person_marital_information': fields.boolean("Show Marital Information",
            implied_group='partner_person.personal_marital_information',
            help="Show Marital Status, Husband and Wife Fields in Personal Information Tab"),        
        'group_person_birthdate': fields.boolean("Show Birthdate",
            implied_group='partner_person.person_birthdate',
            help="Show Birthdate Field in Personal Information Tab"),        
        'group_person_family': fields.boolean("Show Family Information",
            implied_group='partner_person.person_family',
            help="Show Mother, Father and Childs Fields in Personal Information Tab"),
        'group_person_nationality': fields.boolean("Show Nationality",
            implied_group='partner_person.person_nationality',
            help="Show Nationality Field in Personal Information Tab"),        
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
