# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api


class sale_order(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def check_unapproved_partner_ok(self):
        self.ensure_one()
        if self.company_id.restrict_sales == 'yes':
            if self.partner_id.partner_state != 'approved':
                return False
        return True

    @api.multi
    def check_unapproved_partner_amount_ok(self):
        self.ensure_one()
        if self.company_id.restrict_sales == 'amount_depends':
            if (
                    self.partner_id.partner_state != 'approved' and
                    self.amount_total >= self.company_id.restrict_sales_amount
                    ):
                return False
        return True
