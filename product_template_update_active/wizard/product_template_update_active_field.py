# -*- coding: utf-8 -*-
from openerp import models, api


class product_template_update_active_field(models.TransientModel):
    _name = "product.template_update_active_field"
    _description = "product.template_update_active_field"

    @api.one
    def update_all(self):
        templates = self.env['product.template'].search(
            [('active', 'in', [False, True])])
        return self.update_active(templates.ids)

    @api.one
    def update_active_ids(self):
        template_ids = self._context.get('active_ids', [])
        return self.update_active(template_ids)

    @api.one
    def update_active(self, template_ids):
        product_template = self.env['product.template']
        inactive_template_ids = product_template.search([
                ('id', 'in', template_ids),
                ('active', '=', False),
            ]).ids
        to_active_template_ids = []
        to_inactive_template_ids = []
        for template_id in template_ids:
            product_ids = self.env['product.product'].search([
                ('product_tmpl_id', '=', template_id),
                ('active', '=', True),
            ])
            # update to active
            if product_ids and template_id in inactive_template_ids:
                to_active_template_ids.append(template_id)
            # update inactive
            elif not product_ids and template_id not in inactive_template_ids:
                to_inactive_template_ids.append(template_id)

        self.env['product.template'].browse(
            to_inactive_template_ids).write({'active': False})
        self.env['product.template'].browse(
            to_active_template_ids).write({'active': True})
