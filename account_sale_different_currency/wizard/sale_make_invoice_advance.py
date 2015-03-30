# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _


class sale_advance_payment_inv(osv.osv_memory):
    _inherit = "sale.advance.payment.inv"

    _columns = {
        'invoice_currency_rate': fields.float(
            'Invoice Currency Rate',
        ),
        'invoice_currency_id': fields.many2one(
            'res.currency', 'Invoice Currency',
            readonly=True,
        ),
        'invoice_currency_amount': fields.float(
            'Invoice Currency Advance Amount',
            readonly=True,
            digits_compute=dp.get_precision('Account')),
    }

    def _get_invoice_currency_rate(self, cr, uid, context=None):
        sale_id = context.get('active_id', False)
        invoice_currency_rate = False
        if sale_id:
            sale = self.pool['sale.order'].browse(
                cr, uid, sale_id, context=context)
            invoice_currency_rate = self.pool['res.currency'].compute(
                cr, uid, sale.pricelist_id.currency_id.id,
                sale.different_currency_id.id,
                1.0, round=False, context=context)
            invoice_currency_rate = invoice_currency_rate
        return invoice_currency_rate

    def _get_invoice_currency_id(self, cr, uid, context=None):
        sale_id = context.get('active_id', False)
        invoice_currency_id = False
        if sale_id:
            sale = self.pool['sale.order'].browse(
                cr, uid, sale_id, context=context)
            invoice_currency_id = sale.different_currency_id and sale.different_currency_id.id or False
        return invoice_currency_id

    def _get_product_id(self, cr, uid, context=None):
        print 'context', context
        sale_id = context.get('active_id', False)
        product_id = False
        if sale_id:
            sale = self.pool['sale.order'].browse(
                cr, uid, sale_id, context=context)
            product_id = sale.company_id.default_advance_product_id and sale.company_id.default_advance_product_id.id or False
        return product_id

    _defaults = {
        'invoice_currency_rate': _get_invoice_currency_rate,
        'invoice_currency_id': _get_invoice_currency_id,
        'product_id': _get_product_id,
    }

    def onchange_method(
            self, cr, uid, ids,
            advance_payment_method, product_id, context=None):
        # Modificamos esta funcion para poder usar percentage con producto
        # y que no ponga el product en null
        if advance_payment_method == 'percentage':
            return {'value': {'amount': 0}}
            # return {'value': {'amount':0, 'product_id':False }}
        if product_id and advance_payment_method == 'fixed':
            product = self.pool.get('product.product').browse(cr, uid, product_id, context=context)
            return {'value': {'amount': product.list_price}}
        return {'value': {'amount': 0}}

    def create_invoices(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids[0], context)
        if wizard.advance_payment_method in ('lines'):
        # if wizard.advance_payment_method in ('percentage', 'lines'):
            raise osv.except_osv(
                _('Configuration Error!'),
                _("If Invoice in different Currency you can not select 'Percentage' or 'Some order lines'."))
        return super(sale_advance_payment_inv, self).create_invoices(
            cr, uid, ids, context)

    def on_change_currency_amount(
            self, cr, uid, ids, invoice_currency_rate, amount, context=None):
        result = {'domain': {}, 'value': {}}
        invoice_currency_amount = False
        if invoice_currency_rate and amount:
            invoice_currency_amount = amount * invoice_currency_rate
        result['value']['invoice_currency_amount'] = invoice_currency_amount
        return result

    def _prepare_advance_invoice_vals(self, cr, uid, ids, context=None):
        # Intento de heredar y modificar metodo
        # pero que era demasiado complicado
        # result = super(sale_advance_payment_inv, self)._prepare_advance_invoice_vals(
        #     cr, uid, ids, context=context)
        # print 'context', context
        # print 'TODO Agregar el valor del campo de la otra currency'
        # return res
        # for invoice in result:
        #     invoice_values = invoice[1]
        #     print 'invoice_values', invoice_values
        #     invoice_line_values = invoice[1]['invoice_line']
        #     print 'invoice_line_values', invoice_line_values

        # La simplificamos y sobreescribimos completamente
        if context is None:
            context = {}
        sale_obj = self.pool.get('sale.order')
        ir_property_obj = self.pool.get('ir.property')
        fiscal_obj = self.pool.get('account.fiscal.position')
        inv_line_obj = self.pool.get('account.invoice.line')
        wizard = self.browse(cr, uid, ids[0], context)
        sale_ids = context.get('active_ids', [])

        result = []
        for sale in sale_obj.browse(cr, uid, sale_ids, context=context):
            val = inv_line_obj.product_id_change(cr, uid, [], wizard.product_id.id,
                                                 uom_id=False, partner_id=sale.partner_id.id, fposition_id=sale.fiscal_position.id)
            res = val['value']

            # determine and check income account
            if not wizard.product_id.id:
                prop = ir_property_obj.get(cr, uid,
                                           'property_account_income_categ', 'product.category', context=context)
                prop_id = prop and prop.id or False
                account_id = fiscal_obj.map_account(
                    cr, uid, sale.fiscal_position or False, prop_id)
                if not account_id:
                    raise osv.except_osv(_('Configuration Error!'),
                                         _('There is no income account defined as global property.'))
                res['account_id'] = account_id
            if not res.get('account_id'):
                raise osv.except_osv(_('Configuration Error!'),
                                     _('There is no income account defined for this product: "%s" (id:%d).') %
                                     (wizard.product_id.name, wizard.product_id.id,))

            # determine invoice amount
            if wizard.amount <= 0.00:
                raise osv.except_osv(_('Incorrect Data'),
                                     _('The value of Advance Amount must be positive.'))
            if wizard.advance_payment_method == 'percentage':
                # Esta es la parte que modificamos
                inv_amount = sale.amount_untaxed * wizard.amount / 100
                if wizard.invoice_currency_id:
                    sale_currency_price_unit = inv_amount
                    inv_amount = inv_amount * wizard.invoice_currency_rate
                if not res.get('name'):
                    res['name'] = _("Advance of %s %%") % (wizard.amount)
            else:
                # Esta es la parte que modificamos
                # inv_amount = wizard.amount
                sale_currency_price_unit = False
                if wizard.invoice_currency_id:
                    # no uso invoice_currency_amount porque como es readonly
                    # no se guarda
                    inv_amount = wizard.amount * wizard.invoice_currency_rate
                    sale_currency_price_unit = wizard.amount
                else:
                    inv_amount = wizard.amount

                if not res.get('name'):
                    # TODO: should find a way to call formatLang() from
                    # rml_parse
                    symbol = sale.pricelist_id.currency_id.symbol
                    if sale.pricelist_id.currency_id.position == 'after':
                        res['name'] = _("Advance of %s %s") % (
                            inv_amount, symbol)
                    else:
                        res['name'] = _("Advance of %s %s") % (
                            symbol, inv_amount)

            # determine taxes
            if res.get('invoice_line_tax_id'):
                res['invoice_line_tax_id'] = [
                    (6, 0, res.get('invoice_line_tax_id'))]
            else:
                res['invoice_line_tax_id'] = False

            line_name = res.get('name')
            line_name += '. TC: %s' % wizard.invoice_currency_rate
            for line in sale.order_line:
                line_name += '\n* %s' % (line.name)

            # create the invoice
            inv_line_values = {
                'name': line_name,
                'origin': sale.name,
                'account_id': res['account_id'],
                'price_unit': inv_amount,
                'sale_currency_price_unit': sale_currency_price_unit,
                'quantity': wizard.qtty or 1.0,
                'discount': False,
                'uos_id': res.get('uos_id', False),
                'product_id': wizard.product_id.id,
                'invoice_line_tax_id': res.get('invoice_line_tax_id'),
                'account_analytic_id': sale.project_id.id or False,
                'sequence': 99, #las seteamos en 99 asi luego son copiadas con igual sequencia y van al final de todo
            }
            inv_values = {
                'name': sale.client_order_ref or sale.name,
                'origin': sale.name,
                'type': 'out_invoice',
                'reference': False,
                'account_id': sale.partner_id.property_account_receivable.id,
                'partner_id': sale.partner_invoice_id.id,
                'invoice_currency_rate': wizard.invoice_currency_rate,
                'invoice_line': [(0, 0, inv_line_values)],
                # Aca tambien modificamos
                'sale_currency_id': sale.pricelist_id.currency_id.id,
                'currency_id': wizard.invoice_currency_id and wizard.invoice_currency_id.id or sale.pricelist_id.currency_id.id,
                'comment': '',
                'payment_term': sale.payment_term.id,
                'fiscal_position': sale.fiscal_position.id or sale.partner_id.property_account_position.id
            }
            result.append((sale.id, inv_values))
        return result

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
