# -*- coding: utf-8 -*-

from openerp import models, fields


class res_company_partner_state_field(models.Model):
    _name = 'res.company.partner_state_field'
    _description = 'Company Partner State Fields'

    company_id = fields.Many2one(
        'res.company', string='Company', required=True)
    field_id = fields.Many2one(
        'ir.model.fields',
        string='Field',
        required=True,
        domain=[('model_id.model', '=', 'res.partner')])
    approval = fields.Boolean(
        'Approval?',
        help="Required for Approval",
        default=True)
    track = fields.Boolean(
        'Track?',
        help="Track and, if change, go back to Potencial",
        default=True)


class res_company(models.Model):
    _inherit = 'res.company'

    partner_state = fields.Boolean('Use partner state?')
    restrict_sales = fields.Selection(
        [('yes', 'Yes'), ('amount_depends', 'Depends on the amount')],
        'Restrict Sales?', help="Restrict Sales to Unapproved Partners?")
    restrict_sales_amount = fields.Float('Restrict Amounts Greater Than')
    partner_state_field_ids = fields.One2many(
        'res.company.partner_state_field', 'company_id', string='State Fields')
