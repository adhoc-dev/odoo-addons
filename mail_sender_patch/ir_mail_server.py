# -*- coding: utf-8 -*-
from openerp.osv import osv


class ir_mail_server(osv.osv):
    _inherit = "ir.mail_server"

    def _get_default_bounce_address(self, cr, uid, context=None):
        mail_server_ids = self.search(
            cr, uid, [], order='sequence asc', limit=1, context=context)
        print 'mail_server_ids', mail_server_ids
        if mail_server_ids:
            return self.browse(cr, uid, mail_server_ids[0]).smtp_user
        else:
            return super(ir_mail_server, self)._get_default_bounce_address(
                cr, uid, context)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
