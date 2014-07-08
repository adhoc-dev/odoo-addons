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

from lxml import etree
import math
import pytz
import re

import openerp
from openerp import SUPERUSER_ID
from openerp import pooler, tools
from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp.tools.yaml_import import is_comment
from datetime import date, datetime


class res_users(osv.osv):
    _inherit = "res.users"
    # added this here because in v8 there is a conflict with a char birthdate field in partner
    # it is supose to be fixed
    _columns = {
        'birthdate': fields.date(string='Birthdate'),
        }

class res_partner(osv.osv):
    _inherit = "res.partner"

    def _get_age(self, cr, uid, ids, name, args, context=None):
        if context == None:
            context = {}
        res = {}

        today = date.today()
        for record in self.browse(cr, uid, ids, context=context):
            if record.birthdate:
                birthdate = (datetime.strptime(record.birthdate, '%Y-%m-%d')).date()
                try: 
                    birthday = birthdate.replace(year=today.year)
                except ValueError: # raised when birth date is February 29 and the current year is not a leap year
                    birthday = birthdate.replace(year=today.year, day=birthdate.day-1)
                if birthday > today:
                    age = today.year - birthdate.year - 1
                else:
                    age = today.year - birthdate.year                
                res[record.id] = age
            else:
                res[record.id] = False
        return res


    def _get_husband(self, cr, uid, ids, name, args, context=None):
        if context == None:
            context = {}

        res = {}
        for i in ids:
            husband_ids = self.search(cr, uid, [('wife_id','=',i)], context=context)
            husband_id = False
            if husband_ids:
                husband_id = husband_ids[0]
            res[i] = husband_id
        return res

    def _set_wife(self, cr, uid, wife_id, field_name, field_value, arg, context=None):
        husband_ids = self.search(cr, uid, [('wife_id','=',wife_id)], context=context)
        # If wife related to this partner, we set husband = False for those wifes
        self.write(cr, uid, husband_ids, {'wife_id':False}, context=context)

        # We write the husband for the actual wife
        if field_value:
            return self.write(cr, uid, field_value, {'wife_id':wife_id}, context=context)
        return True
        
    _columns = {
        'disabled_person': fields.boolean(string='Disabled Person?'),
        'firstname': fields.char(string='First Name'),
        'lastname': fields.char(string='Last Name'),
        'national_identity': fields.char(string='National Identity'),
        'passport': fields.char(string='Passport'),
        'marital_status': fields.selection([(u'single', u'Single'), (u'married', u'Married'), (u'divorced', u'Divorced')], string='Marital Status'),
        'birthdate': fields.date(string='Birthdate'),
        'father_id': fields.many2one('res.partner', string='Father', context={'default_is_company':False,'default_sex':'M','from_member':True}, domain=[('is_company','=',False),('sex','=','M')]),
        'mother_id': fields.many2one('res.partner', string='Mother', context={'default_is_company':False,'default_sex':'F','from_member':True}, domain=[('is_company','=',False),('sex','=','F')]),
        'sex': fields.selection([(u'M', u'Male'), (u'F', u'Female')], string='Sex'),
        'age': fields.function (_get_age, type='integer', string='Age'),
        'father_child_ids': fields.one2many ('res.partner', 'father_id', string='Childs',),
        'mother_child_ids': fields.one2many ('res.partner', 'mother_id', string='Childs',),
        'nationality_id': fields.many2one('res.country', string='Nationality'),
        'husband_id': fields.function (_get_husband, fnct_inv=_set_wife, type='many2one', relation='res.partner',string='Husband', domain=[('sex','=','M'),('is_company','=',False)], context={'default_sex':'M','is_person':True}),
        'wife_id': fields.many2one ('res.partner', string='Wife', domain=[('sex','=','F'),('is_company','=',False)], context={'default_sex':'F','is_person':True}),
    }

    def write(self, cr, uid, ids, vals, context=None):
        if not ids:
            return False
        if isinstance(ids, (int, long)):
            ids = [ids]
        partner_id = ids[0]
        lastname = vals.get('lastname',False)
        firstname = vals.get('firstname',False)
        if lastname or firstname:
            if not firstname:
                partner = self.browse(cr, uid, partner_id, context=context)
                firstname = partner.firstname
            if not lastname:
                partner = self.browse(cr, uid, partner_id, context=context)
                lastname = partner.lastname
            vals['name'] = (firstname or '' ) + ' ' + (lastname or '')
        result = super(res_partner,self).write(cr, uid, ids, vals, context=context)
        return result

    def create(self, cr, uid, vals, context=None):
        lastname = vals.get('lastname', False)
        firstname = vals.get('firstname', False)
        if lastname or firstname:
            vals['name'] = (firstname or '' ) + ' ' + (lastname or '')
        new_id = super(res_partner, self).create(cr, uid, vals, context=context)
        return new_id

    def onchange_name(self, cr, uid, ids, firstname, lastname, context=None):
        v = {}
        
        v['name'] = (firstname or '' ) + ' ' + (lastname or '')

        return {'value': v}  


    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = []
        for record in self.browse(cr, uid, ids, context=context):
            name = record.name
            national_identity = ''
            if record.national_identity:
                national_identity = '[' + record.national_identity + ']'
            name =  "%s %s" % (national_identity, name)
            if record.parent_id and not record.is_company:
                name =  "%s, %s" % (record.parent_id.name, name)
            if context.get('show_address'):
                name = name + "\n" + self._display_address(cr, uid, record, without_company=True, context=context)
                name = name.replace('\n\n','\n')
                name = name.replace('\n\n','\n')
            if context.get('show_email') and record.email:
                name = "%s <%s>" % (name, record.email)
            res.append((record.id, name))
        return res

    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if name and operator in ('=', 'ilike', '=ilike', 'like', '=like'):
            # search on the name of the contacts and of its company
            search_name = name
            if operator in ('ilike', 'like'):
                search_name = '%%%s%%' % name
            if operator in ('=ilike', '=like'):
                operator = operator[1:]
            query_args = {'name': search_name}
            # TODO: simplify this in trunk with `display_name`, once it is stored
            # Perf note: a CTE expression (WITH ...) seems to have an even higher cost
            #            than this query with duplicated CASE expressions. The bulk of
            #            the cost is the ORDER BY, and it is inevitable if we want
            #            relevant results for the next step, otherwise we'd return
            #            a random selection of `limit` results.
            query = ('''SELECT partner.id FROM res_partner partner
                                          LEFT JOIN res_partner company
                                               ON partner.parent_id = company.id
                        WHERE   partner.national_identity ''' + operator + ''' %(name)s OR 
                                partner.email ''' + operator + ''' %(name)s OR 
                              CASE
                                   WHEN company.id IS NULL OR partner.is_company
                                       THEN partner.name
                                   ELSE company.name || ', ' || partner.name
                              END ''' + operator + ''' %(name)s
                        ORDER BY
                              CASE
                                   WHEN company.id IS NULL OR partner.is_company
                                       THEN partner.name
                                   ELSE company.name || ', ' || partner.name
                              END''')
            if limit:
                query += ' limit %(limit)s'
                query_args['limit'] = limit
            cr.execute(query, query_args)
            ids = map(lambda x: x[0], cr.fetchall())
            ids = self.search(cr, uid, [('id', 'in', ids)] + args, limit=limit, context=context)
            if ids:
                return self.name_get(cr, uid, ids, context)
        return super(res_partner,self).name_search(cr, uid, name, args, operator=operator, context=context, limit=limit)
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
