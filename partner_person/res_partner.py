# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from datetime import date
from openerp.osv import fields as old_fields
from openerp.osv import osv


class res_users(models.Model):
    _inherit = "res.users"
    # added this here because in v8 there is a conflict with a char birthdate
    # field in partner it is supose to be fixed
    birthdate = fields.Date(string='Birthdate')


class res_partner(models.Model):
    _inherit = "res.partner"

    @api.one
    @api.depends('birthdate')
    def _get_age(self):
        today = date.today()
        age = False
        if self.birthdate:
            birthdate = fields.Date.from_string(self.birthdate)
            try:
                birthday = birthdate.replace(year=today.year)
            # raised when birth date is February 29 and the current year is
            # not a leap year
            except ValueError:
                birthday = birthdate.replace(
                    year=today.year, day=birthdate.day - 1)
            if birthday > today:
                age = today.year - birthdate.year - 1
            else:
                age = today.year - birthdate.year
        self.age = age

    @api.one
    # @api.depends('wife_id')
    def _get_husband(self):
        husbands = self.search([('wife_id', '=', self.id)])
        self.husband_id = husbands.id

    def _set_wife(self):
        husbands = self.search([('wife_id', '=', self.id)])
        # If wife related to this partner, we set husband = False for those
        # wifes
        husbands.write({'wife_id': False})

        # We write the husband for the actual wife
        if self.husband_id:
            self.husband_id.wife_id = self.id
            
    def _search_husband(self, operator, value):

        if operator == 'like':
            operator = 'ilike'

        ids = self.search([('wife_id', '!=' , False) ,('name', operator, value )])

        ret=[]
        for result in ids:
            ret.append(result.wife_id.id)

        return [('id', 'in' , ret)]

    disabled_person = fields.Boolean(string='Disabled Person?')
    firstname = fields.Char(string='First Name')
    lastname = fields.Char(string='Last Name')
    national_identity = fields.Char(string='National Identity')
    passport = fields.Char(string='Passport')
    marital_status = fields.Selection(
        [(u'single', u'Single'), (u'married', u'Married'),
         (u'divorced', u'Divorced')], string='Marital Status')
    birthdate = fields.Date(string='Birthdate')
    father_id = fields.Many2one(
        'res.partner', string='Father',
        context={'default_is_company': False, 'default_sex': 'M',
                 'from_member': True},
        domain=[('is_company', '=', False), ('sex', '=', 'M')])
    mother_id = fields.Many2one(
        'res.partner', string='Mother',
        context={'default_is_company': False, 'default_sex': 'F',
                 'from_member': True},
        domain=[('is_company', '=', False), ('sex', '=', 'F')])
    sex = fields.Selection(
        [(u'M', u'Male'), (u'F', u'Female')], string='Sex')
    age = fields.Integer(compute='_get_age', type='integer', string='Age')
    father_child_ids = fields.One2many(
        'res.partner', 'father_id', string='Childs',)
    mother_child_ids = fields.One2many(
        'res.partner', 'mother_id', string='Childs',)
    nationality_id = fields.Many2one('res.country', string='Nationality')
    husband_id = fields.Many2one(
        'res.partner',
        compute='_get_husband',
        inverse='_set_wife',
        search='_search_husband',
        string='Husband',
        domain=[('sex', '=', 'M'), ('is_company', '=', False)],
        context={'default_sex': 'M', 'is_person': True})
    wife_id = fields.Many2one(
        'res.partner', string='Wife',
        domain=[('sex', '=', 'F'), ('is_company', '=', False)],
        context={'default_sex': 'F', 'is_person': True})

    @api.one
    @api.onchange('firstname', 'lastname')
    @api.constrains('firstname', 'lastname')
    def build_name(self):
        print '111111'
        self.name = '%s %s' % (
            self.lastname or '', self.firstname or '')

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
            name = "%s %s" % (name, national_identity)
            if record.parent_id and not record.is_company:
                name = "%s, %s" % (record.parent_id.name, name)
            if context.get('show_address'):
                name = name + "\n" + \
                    self._display_address(
                        cr, uid, record, without_company=True, context=context)
                name = name.replace('\n\n', '\n')
                name = name.replace('\n\n', '\n')
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
            ids = self.search(
                cr, uid, [('id', 'in', ids)] + args, limit=limit, context=context)
            if ids:
                return self.name_get(cr, uid, ids, context)
        return super(res_partner, self).name_search(cr, uid, name, args, operator=operator, context=context, limit=limit)

    # Como no anduvo sobre escribiendo con la nueva api, tuvimos que hacerlo con la vieja
    # display_name = fields.Char(
    #     compute='_display_name', string='Name', store=True, select=True)

    # @api.one
    # @api.depends(
    #     'name',
    #     'firstname',
    #     'lastname',
    #     'is_company',
    #     'national_identity',
    #     'parent_id',
    #     'parent_id.name',
    #     )
    # def _diplay_name(self):
    #     self.display_name = self.with_context({}).name_get()


    _display_name = lambda self, *args, **kwargs: self._display_name_compute(*args, **kwargs)

    _display_name_store_triggers = {
        'res.partner': (lambda self,cr,uid,ids,context=None: self.search(cr, uid, [('id','child_of',ids)], context=dict(active_test=False)),
                        ['parent_id', 'is_company', 'name', 'national_identity'], 10)
        # Se agrega national_identity aqui
    }

    _columns = {
        'display_name': old_fields.function(_display_name, type='char', string='N2222asdasdadsame', store=_display_name_store_triggers, select=True),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
