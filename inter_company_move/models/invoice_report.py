# -*- coding: utf-8 -*-
from openerp import models, fields
# from openerp.osv import fields, osv


# class account_invoice_report(osv.osv):
class account_invoice_report(models.Model):
    _inherit = 'account.invoice.report'

    # _columns = {
    #     'active': fields.boolean('Sales Team'),
    # }
    active = fields.Boolean('Sales Team')

    _depends = {
        'account.invoice': ['active'],
    }

    def _select(self):
        return super(
            account_invoice_report, self)._select() + ", sub.active as active"

    def _sub_select(self):
        return super(
            account_invoice_report, self)._sub_select() + ", ai.active as active"

    def _group_by(self):
        return super(account_invoice_report, self)._group_by() + ", ai.active"
