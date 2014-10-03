# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp.osv import fields as old_fields
from openerp import fields, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.exceptions import Warning
from dateutil import relativedelta
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT


class sale_advance_payment_inv(osv.osv_memory):
    _inherit = "sale.advance.payment.inv"

    first_invoice_date = fields.Date('First Invoice')
    invoice_qty = fields.Integer('Invoices Quantity (one per month)')
    invoices_amount = fields.Float(
        'Amount for each invoie', related="amount",
        readonly=True, digits_compute=dp.get_precision('Account'),)
    _columns = {
        'advance_payment_method': old_fields.selection(
            [('all', 'Invoice the whole sales order'), ('percentage', 'Percentage'), ('fixed', 'Fixed price (deposit)'),
             ('lines', 'Some order lines'), ('multiple', 'Make Multiple Invoices')],
            'What do you want to invoice?', required=True,
            help="""Use Invoice the whole sale order to create the final invoice.
            Use Percentage to invoice a percentage of the total amount.
            Use Fixed Price to invoice a specific amound in advance.
            Use Some Order Lines to invoice a selection of the sales order lines.
            Use Multiple Invoices to generate many invoices."""),
    }
    # TODO la nueva api tiene un bug con el campo selection, por ahora lo dejamos con la vieja
    # advance_payment_method = fields.Selection(
        # [('all', 'Invoice the whole sales order'), ('percentage','Percentage'), ('fixed','Fixed price (deposit)'),
        #     ('lines', 'Some order lines'),('multiple', 'Make Multiple Invoices')],
        # 'What do you want to invoice?', required=True,
        # help="""Use Invoice the whole sale order to create the final invoice.
        #     Use Percentage to invoice a percentage of the total amount.
        #     Use Fixed Price to invoice a specific amound in advance.
        #     Use Some Order Lines to invoice a selection of the sales order lines.
        #     Use Multiple Invoices to generate many invoices.""")

    @api.one
    @api.constrains('invoice_qty')
    def _check_invoice_qty(self):
        if self.invoice_qty <= 1 and self.advance_payment_method == 'multiple':
            raise Warning(_('Invoices Quantity must be greater than 1!'))

    @api.onchange('invoice_qty')
    def onchange_invoice_qty(self):
        active_id = self._context['active_id']
        print 'active_id', active_id
        if not active_id or not self.invoice_qty:
            return False
        amount_untaxed = self.env['sale.order'].search(
            [('id', '=', active_id)]).amount_untaxed
        print 'amount_untaxed', amount_untaxed
        print 'self.invoice_qty', self.invoice_qty
        self.amount = (amount_untaxed / self.invoice_qty)

    def create_invoices(self, cr, uid, ids, context=None):
        sale_obj = self.pool.get('sale.order')
        wizard = self.browse(cr, uid, ids[0], context)
        sale_ids = context.get('active_ids', [])
        invoice_obj = self.pool.get('account.invoice')
        if wizard.advance_payment_method == 'multiple':
            if len(sale_ids) > 1:
                raise Warning(
                    _('Can not use multiple invoices in multiple sales orders at once!'))

            if sale_obj.browse(cr, uid, sale_ids[0], context=context).invoice_ids:
                raise Warning(
                    _('This sale order has already some invoices created!'))

            inv_ids = []
            for invoice_count in range(wizard.invoice_qty - 1):
                for sale_id, inv_values in self._prepare_advance_invoice_vals(cr, uid, ids, context=context):
                    first_invoice_date = datetime.strptime(
                        wizard.first_invoice_date, DEFAULT_SERVER_DATE_FORMAT)
                    invoice_date = (first_invoice_date + relativedelta.relativedelta(
                        months=invoice_count)).strftime(DEFAULT_SERVER_DATE_FORMAT)
                    invoice_id = self._create_invoices(
                        cr, uid, inv_values, sale_id, context=context)
                    invoice_obj.write(
                        cr, uid, invoice_id, {'date_invoice': invoice_date}, context=context)
                    inv_ids.append(invoice_id)

            # create the final invoices of the active sales orders
            invoice_date = (first_invoice_date + relativedelta.relativedelta(
                months=wizard.invoice_qty - 1)).strftime(DEFAULT_SERVER_DATE_FORMAT)
            invoice_id = sale_obj.manual_invoice(
                cr, uid, sale_ids, context).get('res_id', False)
            invoice_obj.write(
                cr, uid, invoice_id, {'date_invoice': invoice_date}, context=context)

            if context.get('open_invoices', False):
                return sale_obj.action_view_invoice(cr, uid, sale_ids, context=context)
            return {'type': 'ir.actions.act_window_close'}
        return super(sale_advance_payment_inv, self).create_invoices(cr, uid, ids, context=context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
