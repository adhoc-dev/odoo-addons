# -*- coding: utf-8 -*-
from openerp import fields, api, models
from openerp.tools.translate import _
from openerp.exceptions import Warning


class account_voucher_receipt(models.Model):

    _name = "account.voucher.receipt"
    _inherit = ['mail.thread']
    _description = 'Account Voucher Receipt'

    @api.one
    @api.depends('voucher_ids', 'voucher_ids.amount')
    def _get_receipt_data(self):
        receipt_amount = 0.0
        has_vouchers = False
        if len(self.voucher_ids) > 0:
            has_vouchers = True
        receipt_amount = sum([x.amount for x in self.voucher_ids])
        self.receipt_amount = receipt_amount
        self.has_vouchers = has_vouchers

    @api.model
    def _get_period(self):
        if self._context.get('period_id', False):
            return self._context.get('period_id')
        periods = self.env['account.period'].find()
        return periods and periods[0] or False

    @api.one
    @api.depends('customer_id', 'supplier_id')
    def _get_partner(self):
        if self.customer_id:
            self.partner_id = self.customer_id.id
        elif self.supplier_id:
            self.partner_id = self.supplier_id.id
        else:
            self.partner_id = False

    @api.model
    def _get_receiptbook(self):
        receiptbook_ids = self.env[
            'account.voucher.receiptbook'].search(
            [('type', '=', self._context.get('type', False))])
        return receiptbook_ids and receiptbook_ids[0] or False

    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        compute="_get_partner")
    name = fields.Char(
        string='Receipt Number',
        size=128,
        required=False,
        readonly=True,
        copy=False
        )
    period_id = fields.Many2one(
        'account.period',
        'Period',
        required=True,
        readonly=True,
        default=_get_period,
        states={'draft': [('readonly', False)]}
        )
    manual_prefix = fields.Char(
        related='receiptbook_id.manual_prefix',
        string='Prefix',
        readonly=True,
        copy=False
        )
    manual_sufix = fields.Integer(
        'Number',
        readonly=True,
        states={'draft': [('readonly', False)]},
        copy=False
        )
    force_number = fields.Char(
        'Force Number',
        readonly=True,
        states={'draft': [('readonly', False)]},
        copy=False)
    receiptbook_id = fields.Many2one(
        'account.voucher.receiptbook',
        'ReceiptBook',
        readonly=True,
        required=True,
        states={'draft': [('readonly', False)]},
        default=_get_receiptbook,
        )
    company_id = fields.Many2one(
        'res.company',
        'Company',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        default=lambda self: self.env[
            'res.company']._company_default_get('account.voucher.receipt')
        )
    date = fields.Date(
        'Receipt Date',
        readonly=True,
        states={'draft': [('readonly', False)]},
        default=fields.Date.context_today,
        )
    supplier_id = fields.Many2one(
        'res.partner',
        domain=[('supplier', '=', True)],
        context={'search_default_supplier': 1},
        string='Supplier',
        readonly=True,
        states={'draft': [('readonly', False)]}
        )
    customer_id = fields.Many2one(
        'res.partner',
        domain=[('customer', '=', True)],
        context={'search_default_customer': 1},
        string='Customer',
        readonly=True,
        states={'draft': [('readonly', False)]}
        )
    type = fields.Selection(
        [('receipt', 'Receipt'), ('payment', 'Payment')],
        'Type',
        required=True
        )
    state = fields.Selection(
        [('draft', 'Draft'), ('posted', 'Posted'), ('cancel', 'Cancel')],
        string='State',
        readonly=True,
        default='draft',
        )
    next_receipt_number = fields.Integer(
        related='receiptbook_id.sequence_id.number_next_actual',
        string='Next Receipt Number',
        readonly=True
        )
    receiptbook_sequence_type = fields.Selection(
        related='receiptbook_id.sequence_type',
        string='Receiptbook Sequence Type',
        readonly=True
        )
    has_vouchers = fields.Boolean(
        compute='_get_receipt_data',
        string='Has Vouchers?',
        )
    receipt_amount = fields.Float(
        compute='_get_receipt_data',
        string='Receipt Amount',
        )
    voucher_ids = fields.One2many(
        'account.voucher',
        'receipt_id',
        string='Payments',
        readonly=True,
        states={'draft': [('readonly', False)]}
        )
    comment = fields.Text(
        'Comment',
        )
    # We add supplier and customer vouchers only to open different views
    # depending on receipt type
    customer_voucher_ids = fields.One2many(
        'account.voucher',
        'receipt_id',
        string='Customer Payments',
        readonly=True,
        states={'draft': [('readonly', False)]}
        )
    supplier_voucher_ids = fields.One2many(
        'account.voucher',
        'receipt_id',
        string='Supplier Payments',
        readonly=True,
        states={'draft': [('readonly', False)]}
        )

    _sql_constraints = [
        ('name_uniq', 'unique(name,type,company_id)',
            'The Receipt Number must be unique per Company!')]

    _order = "date desc, id desc"

    @api.one
    @api.onchange('company_id')
    def on_change_company(self):
        ''' We add this function so that receiptbook_id value and domain is
        updated when company_id is change.'''

        result = {'domain': {}}
        periods = self.env['account.period']
        receiptbooks = self.env['account.voucher.receiptbook']
        if self.company_id and self.type:
            receiptbooks = receiptbooks.search([
                ('company_id', '=', self.company_id.id),
                ('type', '=', self.type)])

            # Update company con context and call find method to get period of
            # selected company
            periods = periods.with_context(
                company_id=self.company_id.id).find()

        receiptbook_domain = [('id', 'in', receiptbooks.ids)]
        self.receiptbook_id = receiptbooks and receiptbooks[0] or False
        self.period_id = periods and periods[0] or False
        result['domain']['receiptbook_id'] = receiptbook_domain

        return result

    @api.multi
    def unlink(self):
        for record in self:
            if record.state == 'posted':
                raise Warning(_('Cannot delete a posted receipt.'))
            for voucher in record.voucher_ids:
                if voucher.state == 'posted':
                    raise Warning(_(
                        'Cannot delete a receipt that has posted vouchers.'))
        return super(account_voucher_receipt, self).unlink()

    @api.one
    def post_receipt(self):
        sequences = self.env['ir.sequence']
        if not self.voucher_ids:
            raise Warning(_('Cannot post a receipt that has no voucher(s).'))
        for voucher in self.voucher_ids:
            if voucher.state != 'posted':
                raise Warning(_(
                    'Cannot post a receipt that has voucher(s) on draft or cancelled state.'))
        if self.force_number:
            name = self.force_number
        elif self.receiptbook_id.sequence_type == 'automatic':
            name = sequences.next_by_id(self.receiptbook_id.sequence_id.id)
        elif self.receiptbook_id.sequence_type == 'manual':
            name = self.manual_prefix + '%%0%sd' % self.receiptbook_id.padding % self.manual_sufix
        self.write({
                'state': 'posted',
                'name': name,
            })
        return True

    @api.multi
    def action_cancel_draft(self):
        self.create_workflow()
        self.write({'state': 'draft'})
        return True

    @api.multi
    def cancel_receipt_and_payments(self):
        for record in self:
            record.voucher_ids.cancel_voucher()
        self.cancel_receipt()
        return True

    @api.multi
    def cancel_receipt(self,):
        self.write({'state': 'cancel'})
        return True

    def new_payment_normal(self, cr, uid, ids, context=None):
        # TODO add on context if dialog or normal and depending on this open on or other view. 
        # Better if only one veiw
        # TODO this function should be only called for one id
        if not ids: return []
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        receipt = self.browse(cr, uid, ids[0], context=context)

        receipt_amount = context.get('receipt_amount', False)
        if receipt_amount:
            residual_amount = receipt_amount * 1.0 - receipt.receipt_amount
            if residual_amount < 0.0:
                residual_amount = 0.0
            context['amount'] = residual_amount

        # Look for a default journal in order to avoid an error on wrong accont selection
        journal_ids = []
        if receipt.company_id:
            domain = [
                ('company_id', '=', receipt.company_id.id),
                ('type', 'in', ('cash', 'bank'))]
            # Esto seria si esta instalado el modulo de direction
            if self.pool['account.journal'].fields_get(cr, uid, ['direction']):
                if context.get('type', False) == 'payment':
                    domain.append(('direction', 'in', [False, 'out']))
                elif context.get('type', False) == 'receipt':
                    domain.append(('direction', 'in', [False, 'in']))
            journal_ids = self.pool['account.journal'].search(
                cr, uid, domain, context=context)

        context['default_partner_id'] = receipt.partner_id.id
        context['default_receipt_id'] = receipt.id
        context['default_date'] = receipt.date
        context['default_period_id'] = receipt.period_id.id
        context['default_receiptbook_id'] = receipt.receiptbook_id.id
        context['default_company_id'] = receipt.company_id.id
        context['default_journal_id'] = journal_ids and journal_ids[0] or False
        context['show_cancel_special'] = True
        context['from_receipt'] = True

        if context.get('type', False) == 'receipt':
            action_vendor = mod_obj.get_object_reference(cr, uid, 'account_voucher', 'action_vendor_receipt')
        elif context.get('type', False) == 'payment':
            action_vendor = mod_obj.get_object_reference(cr, uid, 'account_voucher', 'action_vendor_payment')

        action_vendor_id = action_vendor and action_vendor[1] or False
        action_vendor = act_obj.read(cr, uid, [action_vendor_id], context=context)[0]
        action_vendor['target'] = 'new'
        action_vendor['context'] = context
        action_vendor['views'] = [action_vendor['views'][1], action_vendor['views'][0]]
        return action_vendor
