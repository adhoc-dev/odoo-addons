# -*- coding: utf-8 -*-
import re
import unicodedata
from openerp.osv import osv, fields
from openerp import SUPERUSER_ID
from openerp.tools.translate import _
from openerp.tools import email_split
from openerp.tools import ustr
import string
import random


def extract_email(email):
    """ extract the email address from a user-friendly email address """
    addresses = email_split(email)
    return addresses[0] if addresses else ''

# Inspired by http://stackoverflow.com/questions/517923


def remove_accents(input_str):
    """Suboptimal-but-better-than-nothing way to replace accented
    latin letters by an ASCII equivalent. Will obviously change the
    meaning of input_str and work only for some cases"""
    input_str = ustr(input_str)
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    return u''.join([c for c in nkfd_form if not unicodedata.combining(c)])


class partner(osv.osv):

    """"""

    _inherit = 'res.partner'

    def _retrieve_user(self, cr, uid, ids, arg, karg, context=None):
        """ retrieve the (possibly inactive) user corresponding to wizard_user.partner_id
            @param wizard_user: browse record of model portal.wizard.user
            @return: browse record of model res.users
        """
        context = dict(context or {}, active_test=False)
        res_users = self.pool.get('res.users')
        res = {}
        for i in ids:
            domain = [('partner_id', '=', i)]
            user_ids = res_users.search(cr, uid, domain, context=context)
            user_id = False
            if user_ids:
                user_id = user_ids[0]
            res[i] = user_id
        return res

    _columns = {
        'login': fields.related('related_user_id', 'login', string='Login', type='char', size=64, readonly=True,
                                help="Used to log into the system"),
        'password': fields.related('related_user_id', 'password', string='Password', type='char', size=64, readonly=True,
                                   help="Keep empty if you don't want the user to be able to connect on the system."),
        'related_user_id': fields.function(_retrieve_user, relation='res.users', string='User', type='many2one', ),
        'template_user_id': fields.many2one('res.users', string="Template User", domain=[('active', '=', False)],),
    }

    def open_related_user(self, cr, uid, ids, context=None):
        user_id = self.browse(
            cr, uid, ids[0], context=context).related_user_id.id
        if not user_id:
            return False
        view_ref = self.pool.get('ir.model.data').get_object_reference(
            cr, uid, 'base', 'view_users_form')
        view_id = view_ref and view_ref[1] or False,
        return {
            'type': 'ir.actions.act_window',
            'view_id': view_id,
            'res_model': 'res.users',
            'view_mode': 'form',
            'res_id': user_id,
            'target': 'current',
            # 'flags': {'form': {'action_buttons': True, 'options': {'mode': 'edit'}}}
        }

    def delete_user(self, cr, uid, ids, context=None):
        user_id = self.browse(
            cr, uid, ids[0], context=context).related_user_id.id
        if not user_id:
            return False
        return self.pool.get('res.users').unlink(cr, uid, [user_id], context=context)

    def retrieve_user(self, cr, uid, partner, context=None):
        """ retrieve the (possibly inactive) user corresponding to partner
            @param partner: browse record of model portal.wizard.user
            @return: browse record of model res.users
        """

        context = dict(context or {}, active_test=False)
        res_users = self.pool.get('res.users')
        domain = [('partner_id', '=', partner.id)]
        user_ids = res_users.search(cr, uid, domain, context=context)
        return user_ids

    def quickly_create_user(self, cr, uid, ids, context=None):
        res_users = self.pool.get('res.users')
        # Make this an option
        context = dict(context or {}, no_reset_password=True)
        # TODO Pasar argumentos para activar o desactivar
        create_user = True

        for partner in self.browse(cr, SUPERUSER_ID, ids, context):
            group_ids = []
            if not partner.template_user_id:
                raise osv.except_osv(_('Non template user selected!'),
                                     _('Please define a template user for this partner: "%s" (id:%d).') % (partner.name, partner.id))
            group_ids = [x.id for x in partner.template_user_id.groups_id]
            user_ids = self.retrieve_user(cr, SUPERUSER_ID, partner, context)
            if create_user:
                # create a user if necessary, and make sure it is in the portal
                # group
                if not user_ids:
                    user_ids = [
                        self._create_user(cr, SUPERUSER_ID, partner, context)]
                res_users.write(
                    cr, SUPERUSER_ID, user_ids, {'active': True, 'groups_id': [(6, 0, group_ids)]})
                # prepare for the signup process
                # TODO make an option of this
                # partner.signup_prepare()
                # TODO option to send or not email
                # self._send_email(cr, uid, partner, context)
            elif user_ids:
                # deactivate user
                res_users.write(cr, SUPERUSER_ID, user_ids, {'active': False})

    def _create_user(self, cr, uid, partner, context=None):
        """ create a new user for partner.partner_id
            @param partner: browse record of model partner.user
            @return: browse record of model res.users
        """
        res_users = self.pool.get('res.users')
        # to prevent shortcut creation
        create_context = dict(
            context or {}, noshortcut=True, no_reset_password=True)
        if partner.email:
            login = extract_email(partner.email)
        else:
            login = self._clean_and_make_unique(
                cr, uid, partner.name, context=context)
        values = {
            # 'email': extract_email(partner.email),
            'login': login,
            # 'login': extract_email(partner.email),
            'partner_id': partner.id,
            'company_id': partner.company_id.id,
            'company_ids': [(4, partner.company_id.id)],
            'password': ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)),
            'groups_id': [(6, 0, [])],
        }
        return res_users.create(cr, uid, values, context=create_context)

    def _clean_and_make_unique(self, cr, uid, name, context=None):
        # when an alias name appears to already be an email, we keep the local
        # part only
        name = remove_accents(name).lower().split('@')[0]
        name = re.sub(r'[^\w+.]+', '.', name)
        return self._find_unique(cr, uid, name, context=context)

    def _find_unique(self, cr, uid, name, context=None):
        """Find a unique alias name similar to ``name``. If ``name`` is
           already taken, make a variant by adding an integer suffix until
           an unused alias is found.
        """
        sequence = None
        while True:
            new_name = "%s%s" % (
                name, sequence) if sequence is not None else name
            if not self.pool.get('res.users').search(cr, uid, [('login', '=', new_name)]):
                break
            sequence = (sequence + 1) if sequence else 2
        return new_name

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
