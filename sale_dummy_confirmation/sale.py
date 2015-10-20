# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import api, fields, models, _


class sale_order(models.Model):
    _inherit = 'sale.order'

    dummy_confirmation = fields.Boolean(
        'Dummy Confirmation',
        help="If true, this sale order has been dummy confirmed and can go "
        "back to draft."
        )

    @api.multi
    def get_use_dummy_confirm(self):
        self.ensure_one()
        return self.company_id.sale_order_dummy_confirm

    @api.multi
    def action_button_confirm(self):
        self.ensure_one()
        if self.get_use_dummy_confirm():
            self.write({
                'state': 'done',
                'dummy_confirmation': True
                })
            view_id = self.env['ir.model.data'].xmlid_to_res_id(
                'sale.view_order_form')
            return {
                'type': 'ir.actions.act_window',
                'name': _('Sales Order'),
                'res_model': 'sale.order',
                'res_id': self.id,
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': view_id,
                'target': 'current',
                'nodestroy': True,
            }
        else:
            return super(sale_order, self).action_button_confirm()
