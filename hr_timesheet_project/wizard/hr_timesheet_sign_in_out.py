# -*- coding: utf-8 -*-
from openerp.osv import fields, osv

class hr_so_project(osv.osv_memory):
    _inherit = 'hr.sign.out.project'
    _columns = {
        'account_id': fields.many2one('account.analytic.account', 'Project / Analytic Account', domain=[('type','in',['normal','contract'])]),
        }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
