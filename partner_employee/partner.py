# -*- coding: utf-8 -*-
from openerp import fields, models


class partner(models.Model):
    _inherit = 'res.partner'

    employee = fields.Boolean(
        string='Employee',
        help="Check this box if this contact is a Employee",)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
