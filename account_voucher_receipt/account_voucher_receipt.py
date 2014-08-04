# -*- coding: utf-8 -*-
from openerp.osv import fields as old_fields
from openerp.osv import osv 
from openerp import fields, api
from openerp.tools.translate import _


class account_voucher_receipt (osv.osv):
       
    _name = "account.voucher.receipt" 
    _description = 'Account Voucher Receipt'

    def _get_receipt_data(self, cr, uid, ids, name, args, context=None):
        res = {}
        for receipt in self.browse(cr, uid, ids, context=context):
            receipt_amount = 0.0
            has_vouchers = False
            if receipt.voucher_ids:
                has_vouchers = True
                for voucher in receipt.voucher_ids:
                    receipt_amount += voucher.amount
            res[receipt.id] = {'receipt_amount': receipt_amount, 'has_vouchers': has_vouchers}
        return res

    def _get_period(self, cr, uid, context=None):
        if context is None: context = {}
        if context.get('period_id', False):
            return context.get('period_id')
        periods = self.pool.get('account.period').find(cr, uid, context=context)
        return periods and periods[0] or False        

    partner_id = fields.Many2one('res.partner', string='Partner', compute="_get_partner")

    @api.one
    @api.depends('customer_id','supplier_id')
    def _get_partner(self):
        if self.customer_id:
            self.partner_id = self.customer_id.id
        elif self.supplier_id:
            self.partner_id = self.supplier_id.id
        else:
            self.partner_id = False

    _columns = {
            'name':old_fields.char(string='Receipt Number', size=128, required=False, readonly=True, copy=False),
            'period_id': old_fields.many2one('account.period', 'Period', required=True, readonly=True, states={'draft':[('readonly',False)]}),
            'manual_prefix': old_fields.related('receiptbook_id', 'manual_prefix', type='char', string='Prefix', readonly=True, copy=False),
            'manual_sufix': old_fields.integer('Number', readonly=True, states={'draft':[('readonly',False)]}, copy=False),
            'force_number': old_fields.char('Force Number', readonly=True, states={'draft':[('readonly',False)]}, copy=False),
            'receiptbook_id': old_fields.many2one('account.voucher.receiptbook','ReceiptBook',readonly=True,required=True, states={'draft':[('readonly',False)]}),   
            'company_id': old_fields.many2one('res.company', 'Company', required=True, readonly=True, states={'draft':[('readonly',False)]}),
            'date': old_fields.date('Receipt Date', readonly=True, states={'draft':[('readonly',False)]}),
            'supplier_id':old_fields.many2one('res.partner', domain=[('supplier','=',True)], context={'search_default_supplier': 1}, string='Supplier', readonly=True, states={'draft':[('readonly',False)]}),
            'customer_id':old_fields.many2one('res.partner', domain=[('customer','=',True)], context={'search_default_customer': 1}, string='Customer', readonly=True, states={'draft':[('readonly',False)]}),
            'type': old_fields.selection([('receipt','Receipt'),
                                             ('payment','Payment')],'Type', required=True),
            'state': old_fields.selection([('draft','Draft'),('posted','Posted'),('cancel','Cancel')], string='State', readonly=True,),
            'next_receipt_number': old_fields.related('receiptbook_id', 'sequence_id', 'number_next_actual', type='integer', string='Next Receipt Number', readonly=True),
            'receiptbook_sequence_type': old_fields.related('receiptbook_id', 'sequence_type', type='char', string='Receiptbook Sequence Type', readonly=True),
            'has_vouchers': old_fields.function(_get_receipt_data, type='boolean', string='Has Vouchers?', multi='_get_receipt_data',),
            'receipt_amount': old_fields.function(_get_receipt_data, type='float', string='Receipt Amount', multi='_get_receipt_data',),
            'voucher_ids':old_fields.one2many('account.voucher','receipt_id',string='Payments', readonly=True, states={'draft':[('readonly',False)]}),
            # We add supplier and customer vouchers only to open different views depending on receipt type
            'customer_voucher_ids':old_fields.related('voucher_ids',relation='account.voucher',type='one2many',string='Customer Payments', readonly=True, states={'draft':[('readonly',False)]}),
            'supplier_voucher_ids':old_fields.related('voucher_ids',relation='account.voucher',type='one2many',string='Supplier Payments', readonly=True, states={'draft':[('readonly',False)]}),
                }
                
    _sql_constraints = [('name_uniq','unique(name,type,company_id)','The Receipt Number must be unique per Company!')]

    _order = "date desc, id desc"

    def _get_receiptbook(self, cr, uid, context=None):
        if not context:
            context = {}
        receiptbook_ids = self.pool['account.voucher.receiptbook'].search(cr, uid, [('type','=',context.get('type',False))], context=context)
        return receiptbook_ids and receiptbook_ids[0] or False
    
    _defaults = {
        'receiptbook_id': _get_receiptbook, 
        'date': old_fields.date.context_today,
        'period_id': _get_period,
        'state': 'draft',
        'company_id': lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, 'account.voucher.receipt',context=c),        
    }

    def on_change_company(self, cr, uid, ids, rtype, company_id, context=None):
        ''' We add this function so that receiptbook_id value and domain is updated when 
        company_id is change.'''
        
        if context is None: context = {}

        result = {'domain':{},'value':{}}
        receiptbook_id = False
        receiptbook_ids = []
        
        period_id = False
        period_ids = []
        
        if company_id and rtype:
            receiptbook_ids = self.pool['account.voucher.receiptbook'].search(cr, uid, [('company_id','=',company_id),
                ('type','=',rtype)], context=context)
            if receiptbook_ids:                
                receiptbook_id = receiptbook_ids[0]
            
            # Update company con context and call find method to get period of selected company
            context['company_id'] = company_id
            period_ids = self.pool.get('account.period').find(cr, uid, context=context)
            if period_ids:
                period_id = period_ids[0]

        receiptbook_domain = [('id','in',receiptbook_ids)]
        result['domain']['receiptbook_id'] = receiptbook_domain
        result['value']['receiptbook_id'] = receiptbook_id
        result['value']['period_id'] = period_id

        return result

    def unlink(self, cr, uid, ids, context=None):
        for record in self.browse(cr, uid, ids, context=context):
            if record.state == 'posted':
                raise osv.except_osv(_('Invalid Action!'), _('Cannot delete a posted receipt.'))
            for voucher in record.voucher_ids:
                if voucher.state == 'posted':
                    raise osv.except_osv(_('Invalid Action!'), _('Cannot delete a receipt that has posted vouchers.'))
        return super(account_voucher_receipt, self).unlink(cr, uid, ids, context) 

    def post_receipt(self, cr, uid, ids, context=None):
        obj_sequence = self.pool.get('ir.sequence')
        for receipt in self.browse(cr, uid, ids, context=context):
            if not receipt.voucher_ids:
                raise osv.except_osv(_('Invalid Action!'), _('Cannot post a receipt that has no voucher(s).'))
            for voucher in receipt.voucher_ids:
                if voucher.state != 'posted':
                    raise osv.except_osv(_('Invalid Action!'), _('Cannot post a receipt that has voucher(s) on draft or cancelled state.'))
            if receipt.force_number:
                self.write(cr, uid, [receipt.id], {'name':receipt.force_number}, context=context)                
            elif receipt.receiptbook_id.sequence_type == 'automatic':
                sequence = obj_sequence.next_by_id(cr, uid, receipt.receiptbook_id.sequence_id.id, context=context)
                self.write(cr, uid, [receipt.id], {'name':sequence}, context=context)                
            elif receipt.receiptbook_id.sequence_type == 'manual':
                name = receipt.manual_prefix + '%%0%sd' % receipt.receiptbook_id.padding % receipt.manual_sufix
                self.write(cr, uid, [receipt.id], {'name':name}, context=context)
            self.write(cr, uid, [receipt.id], {'state': 'posted'}, context=context)
        return True

    def on_change_receiptbook(self, cr, uid, ids, receiptbook_id, context=None):
        values = {}
        if receiptbook_id:
            receiptbook = self.pool['account.voucher.receiptbook'].browse(cr, uid, receiptbook_id, context=context)
            sequence_type = receiptbook.sequence_type
            values['receiptbook_sequence_type'] = sequence_type
            if sequence_type == 'automatic' and receiptbook.sequence_id:
                values['next_receipt_number'] = receiptbook.sequence_id.number_next_actual
            elif sequence_type == 'manual':
                values['manual_prefix'] = receiptbook.manual_prefix
        else:
            values['receiptbook_sequence_type'] = False
        return {'value':values}

    def action_cancel_draft(self, cr, uid, ids, context=None):
        self.create_workflow(cr, uid, ids)
        self.write(cr, uid, ids, {'state':'draft'})
        return True

    def cancel_receipt_and_payments(self, cr, uid, ids, context=None):
        for receipt in self.browse(cr, uid, ids, context=context):
            voucher_ids = [voucher.id for voucher in receipt.voucher_ids]   
            print 'voucher_ids', voucher_ids
            self.pool['account.voucher'].cancel_voucher(cr, uid, voucher_ids, context=context)
        self.cancel_receipt(cr, uid, ids, context)
        return True

    def cancel_receipt(self, cr, uid, ids, context=None):
        res = {
            'state':'cancel',
        }
        self.write(cr, uid, ids, res)
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
        
        context['default_partner_id'] = receipt.partner_id.id
        context['default_receipt_id'] = receipt.id
        context['default_date'] = receipt.date
        context['default_period_id'] = receipt.period_id.id
        context['default_receiptbook_id'] = receipt.receiptbook_id.id
        context['default_company_id'] = receipt.company_id.id
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
        action_vendor['views'] = [action_vendor['views'][1],action_vendor['views'][0]]
        return action_vendor        