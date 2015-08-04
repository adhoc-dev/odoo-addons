# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class adhoc_base_configuration(models.TransientModel):
    _inherit = 'adhoc.base.config.settings'

    module_website_logo = fields.Boolean(
        'Load a logo image to be used on website only.',
        help="""Installs the website_logo module.""")
    module_website_sale_collapse_categories = fields.Boolean(
        'Changes categories list to allow to collapse them.',
        help="""Installs the website_sale_collapse_categories module.""")
    module_website_sale_vat_required = fields.Boolean(
        'Extends checkout e-commerce form in order to force user to fill "VAT number" field.',
        help="""Installs the website_sale_vat_required module.""")
