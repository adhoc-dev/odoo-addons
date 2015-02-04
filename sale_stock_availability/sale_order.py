# -*- coding    : utf-8 -*-
from openerp import fields, models, api, _


class sale_order_line(models.Model):
    _inherit = "sale.order.line"

    @api.one
    @api.depends(
        'product_uom_qty',
        'product_id')
    def _fnct_line_stock(self):
        available = False
        if self.order_id.state == 'draft':
            available = self.with_context(
                warehouse=self.order_id.warehouse_id.id
            ).product_id.virtual_available - self.product_uom_qty
        self.virtual_available = available
        if available >= 0.0:
            available = True
        else:
            available = False
        self.virtual_available_boolean = available

    virtual_available = fields.Float(
        compute="_fnct_line_stock", string='Saldo Stock')
    virtual_available_boolean = fields.Boolean(
        compute="_fnct_line_stock", string='Saldo Stock')

    def product_id_change_with_wh(
            self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False,
            fiscal_position=False, flag=False, warehouse_id=False,
            context=None):
        res = super(sale_order_line, self).product_id_change_with_wh(
            cr, uid, ids, pricelist, product, qty,
            uom, qty_uos, uos, name, partner_id,
            lang, update_tax, date_order, packaging, fiscal_position, flag,
            warehouse_id=warehouse_id, context=context)

        disable_warning = warehouse_id and self.pool['stock.warehouse'].browse(
            cr, uid, warehouse_id, context).disable_sale_stock_warning or False

        # if not stock warning set in company and warning in res...
        if res.get('warning', False) and disable_warning:
            # clean warning
            warning = {}
            # call sale_stock module other warning
            res_packing = self.product_packaging_change(
                cr, uid, ids, pricelist, product, qty, uom, partner_id,
                packaging, context=context)
            res['value'].update(res_packing.get('value', {}))
            warning_msgs = res_packing.get(
                'warning') and res_packing['warning']['message'] or ''

            if warning_msgs:
                warning = {
                           'title': _('Configuration Error!'),
                           'message': warning_msgs
                        }
            else:
                # if not sale stock warning_try sale warnings
                product_change_res = self.product_id_change(
                    cr, uid, ids, pricelist, product, qty=qty, uom=False,
                    qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
                    lang=lang, update_tax=update_tax, date_order=date_order,
                    packaging=packaging, fiscal_position=fiscal_position,
                    flag=flag, context=context)
                warning = product_change_res.get('warning')
            res.update({'warning': warning})
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
