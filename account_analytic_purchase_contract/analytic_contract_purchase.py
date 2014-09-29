# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _


class account_analytic_purchase(osv.osv):
    _inherit = "account.analytic.account"

    _columns = {

       'type': fields.selection([('view','Analytic View'),
        ('normal','Analytic Account'),
        ('contract','Contract or Project'),
        ('template','Template of Contract'),
        ('purchase_contract','Purchase Contract')], 
        'Type of Account', required=True, help="If you select the View Type, it means you won\'t allow to create journal entries using that account.\n"\
                                  "The type 'Analytic account' stands for usual accounts that you only want to use in accounting.\n"\
                                  "If you select Contract or Project, it offers you the possibility to manage the validity and the invoicing options for this account.\n"\
                                  "The special type 'Template of Contract' allows you to define a template with default data that you can reuse easily."\
                                  "oosdfsdf"),
       }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
