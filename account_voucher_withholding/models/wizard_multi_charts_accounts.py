# -*- coding: utf-8 -*-
from openerp import models, api, fields
import logging
_logger = logging.getLogger(__name__)


class wizard_multi_charts_accounts(models.TransientModel):
    _inherit = 'wizard.multi.charts.accounts'

    tax_template_ids = fields.One2many(
        'account.tax.template',
        'chart_template_id',
        'Withholding Template List',
        help='List of all the withholding that have to be installed by the wizard'
        )

    @api.model
    def _load_template(
            self, template_id, company_id, code_digits=None, obj_wizard=None,
            account_ref=None, taxes_ref=None, tax_code_ref=None):
        """
        Modificamos load template para que luego de cargar todos los datos
        oficiales del plan de cuenta cargue tambien las cuentas de retenciones.
        Agregamos withholding_ref por si llega a ser util utilizarlo en algun
        lugar mas adelante
        """
        res = super(wizard_multi_charts_accounts, self).asda(
            template_id, company_id, code_digits, obj_wizard,
            account_ref, taxes_ref, tax_code_ref)
        withholding_ref = {}
        withholding_ref.update(
            self.env['account.chart.template'].browse(
                template_id).tax_template_ids._generate_withholding(
                tax_code_ref, account_ref, company_id))
        return res
