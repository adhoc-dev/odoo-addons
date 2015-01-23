# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp import models, fields, _, SUPERUSER_ID


class account_invoice(models.Model):
    _inherit = 'account.invoice'

    active = fields.Boolean('Active', default=True)
    invoice_move_type = fields.Selection(
        related='company_id.invoice_move_type',
        string='Invoice Move Type',)
    moved_invoice_id = fields.Many2one(
        'account.invoice', 'Moved Invoice', readonly=True, copy=False)

    def invoice_move(self, cr, uid, ids, context=None):
        for invoice in self.browse(cr, uid, ids, context=context):
            if invoice.invoice_move_type == 'move_wizard':
                mod_obj = self.pool['ir.model.data']
                act_obj = self.pool['ir.actions.act_window']
                action = mod_obj.get_object_reference(
                    cr, uid, 'inter_company_move', 'action_intercompany_move')
                action_id = action and action[1] or False
                action = act_obj.read(cr, uid, [action_id], context=context)[0]
                return action
            elif invoice.invoice_move_type == 'move_auto':
                move_company = invoice.company_id.invoice_move_company_id
                return self._invoice_move(
                    cr, uid, invoice, move_company, context=context)

    def _invoice_move(self, cr, uid, invoice, move_company, context=None):
        """
        TODO
        """
        moved_invoice_id = self.action_create_invoice(
            cr, SUPERUSER_ID, invoice, move_company, invoice.type,
            invoice.journal_id.type, context=context)

        if invoice.company_id.record_moved_id:
            invoice.write({'moved_invoice_id': moved_invoice_id})
        if invoice.company_id.deactivate_invoice:
            invoice.write({'active': False})

        moved_description = _(
            'Moved to invoice id: ') + str(moved_invoice_id)
        invoice.write({
            'internal_number': moved_description,
            'name': moved_description,
        })

        # Cancelamos la factura
        self.signal_workflow(cr, uid, [invoice.id], 'invoice_cancel')

        # sacamos la excepecion de las sales orders
        sale_order_obj = self.pool['sale.order']
        sale_order_ids = sale_order_obj.search(
            cr, uid, [('invoice_ids', 'in', [invoice.id])], context=context)
        self.pool['sale.order'].signal_workflow(
            cr, uid, sale_order_ids, 'invoice_corrected')

        # Si esta seteado asi, retornamos una accion de ventana par ver la
        # factura
        if invoice.company_id.open_after_move:
            return self.action_view_invoice(
                cr, uid, [moved_invoice_id], invoice.type, context=context)
        return True

    def action_view_invoice(self, cr, uid, ids, inv_type=False, context=None):
        '''
        This function returns an action that display moved invoice
        '''
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')

        if inv_type in ['out_invoice', 'out_refund']:
            action = 'action_invoice_tree1'
            form_view = 'invoice_form'
        else:
            action = 'action_invoice_tree2'
            form_view = 'invoice_supplier_form'

        result = mod_obj.get_object_reference(cr, uid, 'account', action)
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]
        # choose the view_mode accordingly
        if len(ids) > 1:
            result[
                'domain'] = "[('id','in',[" + ','.join(map(str, ids)) + "])]"
        else:
            res = mod_obj.get_object_reference(cr, uid, 'account', form_view)
            result['views'] = [(res and res[1] or False, 'form')]
            result['res_id'] = ids and ids[0] or False
        return result

    def action_create_invoice(
            self, cr, uid, invoice, company,
            inv_type, journal_type, context=None):
        if context is None:
            context = {}
        inv_obj = self.pool.get('account.invoice')
        inv_line_obj = self.pool.get('account.invoice.line')

        ctx = context.copy()
        ctx['force_company'] = company.id
        inv_lines = []
        for line in invoice.invoice_line:
            # To find lot of data from product onchanges because its already
            # avail method in core.
            product_uom = line.product_id.uom_id and line.product_id.uom_id.id or False
            line_data = inv_line_obj.product_id_change(
                cr, uid, [line.id], line.product_id.id, product_uom,
                qty=line.quantity, name='', type=inv_type,
                partner_id=invoice.commercial_partner_id.id,
                fposition_id=invoice.commercial_partner_id.property_account_position.id,
                context=ctx, company_id=company.id)
            if not line_data['value'].get('account_id', False):
                account_id = inv_line_obj._default_account(cr, uid, ctx).id
                line_data['value']['account_id'] = account_id
            inv_line_data = self._prepare_inv_line(
                cr, uid, line_data, line, context=ctx)
            inv_line_id = inv_line_obj.create(
                cr, uid, inv_line_data, context=ctx)
            inv_lines.append(inv_line_id)

        # create invoice
        invoice_vals = self._prepare_inv(
            cr, uid, invoice, inv_lines, inv_type, journal_type, company, context=ctx)
        return inv_obj.create(cr, uid, invoice_vals, context=ctx)

    def _prepare_inv_line(self, cr, uid, line_data, line, context=None):
        """ Generate invoice line dictionary"""
        vals = {
            'name': line.name,
            'price_unit': line.price_unit,
            'quantity': line.quantity,
            'discount': line.discount,
            'product_id': line.product_id.id or False,
            'uos_id': line.uos_id.id or False,
            'sequence': line.sequence,
            'invoice_line_tax_id': [
                (6, 0, line_data['value'].get('invoice_line_tax_id', []))],
            'account_analytic_id': line.account_analytic_id.id or False,
        }
        if line_data['value'].get('account_id', False):
            vals['account_id'] = line_data['value']['account_id']
        return vals

    def _prepare_inv(self, cr, uid, invoice, inv_lines, inv_type, jrnl_type, company, context=None):
        """ Generate invoice dictionary """
        context = context or {}
        journal_obj = self.pool.get('account.journal')
        period_obj = self.pool.get('account.period')

        # To find journal.
        journal_ids = journal_obj.search(
            cr, uid,
            [('type', '=', jrnl_type), ('company_id', '=', company.id)],
            limit=1)
        if not journal_ids:
            raise osv.except_osv(_('Error!'),
                                 _('Please define %s journal for this company: "%s" (id:%d).') % (jrnl_type, company.name, company.id))
        # To find periods of supplier company.
        ctx = context.copy()
        ctx.update(company_id=company.id)
        period_ids = period_obj.find(
            cr, uid, invoice.date_invoice, context=ctx)
        # To find account,payment term,fiscal position,bank.
        partner_data = self.onchange_partner_id(
            cr, uid, [invoice.id], inv_type, invoice.commercial_partner_id.id, company_id=company.id)

        return {
            'name': invoice.name,
            'type': inv_type,
            'date_invoice': invoice.date_invoice,
            'account_id': partner_data['value'].get('account_id', False),
            'partner_id': invoice.partner_id.id,
            'user_id': invoice.user_id.id,
            'journal_id': journal_ids[0],
            'invoice_line': [(6, 0, inv_lines)],
            'currency_id': invoice.currency_id and invoice.currency_id.id,
            'fiscal_position': partner_data['value'].get('fiscal_position', False),
            'payment_term': partner_data['value'].get('payment_term', False),
            'company_id': company.id,
            'comment': invoice.comment,
            'period_id': period_ids and period_ids[0] or False,
            'partner_bank_id': partner_data['value'].get('partner_bank_id', False),
        }
