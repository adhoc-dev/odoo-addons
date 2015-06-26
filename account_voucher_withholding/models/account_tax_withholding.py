# -*- coding: utf-8 -*-
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class account_tax_withholding(models.Model):
    _name = "account.tax.withholding"
    _description = "Account Withholding Taxes"

    name = fields.Char(
        'Name',
        required=True,
        )
    description = fields.Char(
        'Description',
        required=True,
        )
    type_tax_use = fields.Selection(
        [('receipt', 'Receipt'), ('payment', 'Payment'), ('all', 'All')],
        'Tax Application',
        required=True
        )
    active = fields.Boolean(
        'Active',
        default=True,
        help="If the active field is set to False, it will allow you to hide the tax without removing it.")
    # TODO add this field  and other for automation
    # type = fields.Selection(
    #     [('percent', 'Percentage'), ('fixed', 'Fixed Amount'),
    #      ('none', 'None'), ('code', 'Python Code'), ('balance', 'Balance')],
    #     'Type',
    #     required=True,
    #     help="The computation method for the tax amount."
    #     )
    account_id = fields.Many2one(
        'account.account',
        'Account',
        required=True,
        )
    ref_account_id = fields.Many2one(
        'account.account',
        'Refund Account',
        required=True,
        )
    account_analytic_id = fields.Many2one(
        'account.analytic.account',
        'Analytic Account',
        )
    ref_account_analytic_id = fields.Many2one(
        'account.analytic.account',
        'Refund Analytic Account',
        )
    company_id = fields.Many2one(
        'res.company',
        'Company',
        required=True,
        default=lambda self: self.env['res.company']._company_default_get(
            'account.tax.withholding')
        )
    #
    # Fields used for the Tax declaration
    #
    # TODO ver si necesitamos los base o no
    base_code_id = fields.Many2one(
        'account.tax.code',
        'Base Code',
        help="Use this code for the tax declaration."
        )
    tax_code_id = fields.Many2one(
        'account.tax.code',
        'Tax Code',
        required=True,
        help="Use this code for the tax declaration.",
        )
    base_sign = fields.Float(
        'Base Code Sign',
        help="Usually 1 or -1.",
        digits_compute=dp.get_precision('Account'),
        )
    tax_sign = fields.Float(
        'Tax Code Sign',
        help="Usually 1 or -1.",
        digits_compute=dp.get_precision('Account'),
        )
    ref_base_code_id = fields.Many2one(
        'account.tax.code',
        'Refund Base Code',
        help="Use this code for the tax declaration."
        )
    ref_tax_code_id = fields.Many2one(
        'account.tax.code',
        'Refund Tax Code',
        required=True,
        help="Use this code for the tax declaration.",
        )
    ref_base_sign = fields.Float(
        'Refund Base Code Sign',
        help="Usually 1 or -1.",
        digits_compute=dp.get_precision('Account'),
        )
    ref_tax_sign = fields.Float(
        'Refund Tax Code Sign',
        help="Usually 1 or -1.",
        digits_compute=dp.get_precision('Account'),
        )


class account_tax_withholding_template(models.Model):
    _name = "account.tax.withholding.template"
    _inherit = "account.tax.withholding"
    _description = "Account Withholding Taxes Template"

    chart_template_id = fields.Many2one(
        'account.chart.template',
        'Chart Template',
        required=True
        )

    @api.multi
    def _generate_withholding(
            self, tax_code_ref, account_ref, company_id):
        """
        This method generate taxes from templates.

        :param self: list of browse record of the tax templates to process
        :param tax_code_template_ref: Taxcode templates reference.
        :param company_id: id of the company the wizard is running for
        :returns:
            {
            'tax_template_to_tax': mapping between tax template and the newly generated taxes corresponding,
            'account_dict': dictionary containing a to-do list with all the accounts to assign on new taxes
            }
        """
        res = {}
        todo_dict = {}
        tax_template_to_tax = {}
        for tax in self:
            vals_tax = {
                'name': tax.name,
                'code': tax.sequence,
                'base_code_id': tax.base_code_id and ((tax.base_code_id.id in tax_code_template_ref) and tax_code_template_ref[tax.base_code_id.id]) or False,
                'tax_code_id': tax.tax_code_id and ((tax.tax_code_id.id in tax_code_template_ref) and tax_code_template_ref[tax.tax_code_id.id]) or False,
                'base_sign': tax.base_sign,
                'tax_sign': tax.tax_sign,
                'base_code_id': tax.ref_base_code_id and ((tax.ref_base_code_id.id in tax_code_template_ref) and tax_code_template_ref[tax.ref_base_code_id.id]) or False,
                'tax_code_id': tax.ref_tax_code_id and ((tax.ref_tax_code_id.id in tax_code_template_ref) and tax_code_template_ref[tax.ref_tax_code_id.id]) or False,
                'base_sign': tax.ref_base_sign,
                'tax_sign': tax.ref_tax_sign,
                'company_id': company_id,
                'account_id': company_id,
                'account_id': company_id,
            }
            new_tax = self.env['account.tax.withholding'].create(vals_tax)
            tax_template_to_tax[tax.id] = new_tax
            #as the accounts have not been created yet, we have to wait before filling these fields
            todo_dict[new_tax] = {
                'account_collected_id': tax.account_collected_id and tax.account_collected_id.id or False,
                'account_paid_id': tax.account_paid_id and tax.account_paid_id.id or False,
            }
        res.update({'tax_template_to_tax': tax_template_to_tax, 'account_dict': todo_dict})
        return res