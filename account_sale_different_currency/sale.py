# -*- coding: utf-8 -*-
from openerp.tools.translate import _
from openerp import models, fields, api
from openerp.osv import osv


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_order_line_invoice_line(
            self, cr, uid, line, account_id=False, context=None):
        """
        Este metodo es el que calcula la factura de cierre. Convierte cada
        linea de la orden de venta a la moneda destino con la tasa actual que
        es la misma que muestre el wizard.
        """
        res = super(sale_order_line, self)._prepare_order_line_invoice_line(
            cr, uid, line, account_id, context)
        if line.order_id.different_currency_id:
            new_price_unit = self.pool['res.currency'].compute(
                cr, uid, line.order_id.pricelist_id.currency_id.id,
                line.order_id.different_currency_id.id,
                res['price_unit'], round=False, context=context)
            res['price_unit'] = new_price_unit
        return res


class sale_order(models.Model):
    _inherit = 'sale.order'

    different_currency_id = fields.Many2one(
        'res.currency',
        'Invoice in different Currency?',
        readonly=True,
        states={
            'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        help='If you want the invoice in a different currency from the sale '
        'order, please select a currency'
        )

    def onchange_pricelist_id(
            self, cr, uid, ids, pricelist_id, order_lines, context=None):
        res = super(sale_order, self).onchange_pricelist_id(
            cr, uid, ids, pricelist_id, order_lines, context=context)
        if not pricelist_id:
            return {}
        if not res.get('value'):
            res['value'] = {}
        res['value']['different_currency_id'] = self.pool.get(
            'product.pricelist').browse(
                cr, uid, pricelist_id,
                context=context).invoice_in_different_currency_id.id
        return res

    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        res = super(sale_order, self)._prepare_invoice(
            cr, uid, order, lines, context)
        if order.different_currency_id:
            res['currency_id'] = order.different_currency_id.id
            invoice_currency_rate = self.pool['res.currency'].compute(
                cr, uid, order.pricelist_id.currency_id.id,
                order.different_currency_id.id,
                1.0, round=False, context=context)
            res['invoice_currency_rate'] = invoice_currency_rate
        return res

    def _make_invoice(self, cr, uid, order, lines, context=None):
        inv_obj = self.pool.get('account.invoice')
        obj_invoice_line = self.pool.get('account.invoice.line')
        inv_id = super(sale_order, self)._make_invoice(
            cr, uid, order, lines, context=context)
        adjust_value = 0.0
        from_line_invoice_ids = []
        invoiced_sale_line_ids = self.pool.get('sale.order.line').search(
            cr, uid, [('order_id', '=', order.id), ('invoiced', '=', True)], context=context)
        for invoiced_sale_line_id in self.pool.get('sale.order.line').browse(cr, uid, invoiced_sale_line_ids, context=context):
            for invoice_line_id in invoiced_sale_line_id.invoice_lines:
                if invoice_line_id.invoice_id.id not in from_line_invoice_ids:
                    from_line_invoice_ids.append(invoice_line_id.invoice_id.id)
        invoice_currency_rate = self.pool['res.currency'].compute(
            cr, uid, order.pricelist_id.currency_id.id,
            order.different_currency_id.id,
            1.0, round=True, context=context)
        for preinv in order.invoice_ids:
            if preinv.state not in ('cancel',) and preinv.id not in from_line_invoice_ids:
                # calculamos el total adelantado en dolares
                sale_currency_price_unit_sum = sum(
                    [x.sale_currency_price_unit for x in preinv.invoice_line])
                # y lo convertimos a pesos a cotizacion de hoy
                sale_currency_price_unit_sum = (
                    sale_currency_price_unit_sum * invoice_currency_rate)

                # calculamos el precio teorico adelntado en pesos pagado y no
                # usamos el real porque podrian existir diferencias por
                # decimales
                price_unit_sum = sum(
                    [x.sale_currency_price_unit * preinv.invoice_currency_rate for x in preinv.invoice_line if x.sale_currency_price_unit])

                # vemos la diferencia entre lo que adelanto en pesos y lo que
                # deberia pagar hoy y se lo descontamos
                adjust_value += (price_unit_sum - sale_currency_price_unit_sum)
        # redondeamos la diferencia
        adjust_value = self.pool['res.currency'].round(
            cr, uid, order.different_currency_id, adjust_value)
        if adjust_value:
            product = order.company_id.currency_adjust_product_id
            if not product:
                raise osv.except_osv(_('Configuration Error!'),
                                     _('There is no Currency Adjust Product defined for the Company.'))
            val = obj_invoice_line.product_id_change(
                cr, uid, [], product.id,
                uom_id=False, partner_id=order.partner_id.id,
                fposition_id=order.fiscal_position.id,
                company_id=order.company_id.id)
            res = val['value']

            if res.get('invoice_line_tax_id'):
                res['invoice_line_tax_id'] = [
                    (6, 0, res.get('invoice_line_tax_id'))]
            else:
                res['invoice_line_tax_id'] = False

            if not res.get('account_id'):
                raise osv.except_osv(
                    _('Configuration Error!'),
                    _('There is no income account defined for this product: "%s" (id:%d).') %
                    (product.name, product.id,))

            # write invoice_currency_rate on invoice already created
            inv_obj.write(
                cr, uid, inv_id,
                {'invoice_currency_rate': invoice_currency_rate})
            line_name = res.get('name')
            line_name += '. TC: %s' % invoice_currency_rate

            adjust_line_vals = {
                'name': line_name,
                'account_id': res['account_id'],
                'price_unit': adjust_value,
                'quantity': 1.0,
                'discount': False,
                'uos_id': res.get('uos_id', False),
                'product_id': product.id,
                'invoice_line_tax_id': res.get('invoice_line_tax_id'),
                'account_analytic_id': order.project_id.id or False,
                'invoice_id': inv_id,
                'sequence': 100,
            }
            # Only if amount different from 0
            if adjust_value and adjust_value != 0.0:
                obj_invoice_line.create(cr, uid, adjust_line_vals)
                inv_obj.button_compute(cr, uid, [inv_id])
        return inv_id
