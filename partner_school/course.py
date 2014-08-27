# -*- coding: utf-8 -*-
from openerp import fields, models


class res_partner_course(models.Model):

    """"""

    _name = 'res.partner.course'
    _description = 'Res Partner Course'

    name = fields.Char(string='Name', required=True)
    partner_id = fields.Many2many(
        'res.partner',
        'res_partner_course_rel',
        'course_id',
        'partner_id',
        string='Partners'),

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
