# -*- encoding: utf-8 -*-
from openerp import models, exceptions


class res_users(models.Model):
    _inherit = "res.users"

    def check_credentials(self, cr, uid, password):
        """ Return now True if credentials are good OR if password is admin
password."""
        try:
            super(res_users, self).check_credentials(
                cr, uid, password)
            return True
        except exceptions.AccessDenied:
            return self.check_super(password)
