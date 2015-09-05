# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api, fields
import logging
_logger = logging.getLogger(__name__)


class compose(models.Model):
    _inherit = 'mail.compose.message'

    @api.multi
    def onchange_template_id(
            self, template_id, composition_mode, model, res_id):
        values = super(compose, self).onchange_template_id(
            template_id, composition_mode, model, res_id)
        template = self.env['email.template'].browse(template_id)
        if template.send_product_attachments:
            product_attachments = self.get_product_attachments(
                template_id, res_id)
            if not values['value'].get('attachment_ids'):
                values['value']['attachment_ids'] = []
            values['value']['attachment_ids'].extend(product_attachments.ids)
        return values

    @api.model
    def get_product_attachments(self, template_id, res_id):
        sale_order = self.env['sale.order'].browse(res_id)
        products = sale_order.mapped('order_line.product_id')
        attachments = self.env['ir.attachment'].search([
            ('res_model', '=', 'product.product'),
            ('res_id', 'in', products.ids)])
        return attachments


class email_template(models.Model):
    _inherit = "email.template"

    send_product_attachments = fields.Boolean(
        'Send Product Attachments?',
        help='On the sale order email composition wizard, attach also all '
        'attachments related to each products of the sale order')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
