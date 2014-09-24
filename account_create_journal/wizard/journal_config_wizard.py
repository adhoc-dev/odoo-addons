# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import logging

_logger = logging.getLogger(__name__)

# Help functions
def find_string(string, array):
  for item in array:
    if string.lower().find(item) == 0:
      return True
  return False

def get_global_type_data(global_type):
  direction = False
  code = '' 
  if global_type == 'issue_check':
    direction = 'out'
    code = 'C' 
  elif global_type == 'third_check':
    direction = False
    code = 'V'
  elif global_type == 'credit_card':
    direction = 'in'
    code = 'T'
  elif global_type == 'bank':
    direction = False
    code = 'B'
  elif global_type == 'cash':
    direction = False
    code = 'C'
  elif global_type == 'tax':
    direction = 'out'
    code = 'R'
  return (direction, code)

def get_global_type(account):
  # Default Value
  global_type = 'bank'
  if find_string(account.name, ['valor','cartera','3ro', 'tercer','third','deposi']):
    global_type = 'third_check'
  elif find_string(account.name, ['chec','propio','own']):
    global_type = 'issue_check'
  elif find_string(account.name, ['credit','card', 'tarjeta']):
    global_type = 'credit_card'
  elif find_string(account.name, ['bank','banco','ahorro','corriente']):
    global_type = 'bank'
  elif find_string(account.name, ['cash','efec','fondo','fijo','caja']):
    global_type = 'cash'
  elif find_string(account.name, ['imp','gana', 'reten', 'tax']):
    global_type = 'tax'
  return global_type

def get_journal_data(point_of_sale, code_sufix, name_prefix, name_sufix, account, global_type=False):
  # Name
  name = account.name
  if name_prefix:
    name = name_prefix + name
  if name_sufix:
    name += name_sufix
  
  # Global Type
  if not global_type:
    global_type = get_global_type(account)
  direction, code = get_global_type_data(global_type)
  
  # Code
  if code_sufix:
    code += code_sufix 
  code += '%%0%sd' % 2 % point_of_sale
  
  # Check and type data 
  journal_type = 'bank'
  use_issued_check = False
  use_third_check = False
  validate_only_checks= False
  if global_type == 'issue_check':
    use_issued_check = True
    validate_only_checks= True
  elif global_type == 'third_check':
    use_third_check = True
    validate_only_checks = True
  elif global_type == 'cash':
    journal_type = 'cash'

  vals = {
    'name': name,
    'code': code,
    'direction': direction,
    'global_type': global_type,
    'account_id': account.id,
    # 'default_debit_account_id': account.id,
    # 'default_credit_account_id': account.id,
    'update_posted': True,
    'allow_date': True,
    'use_issued_check': use_issued_check,
    'validate_only_checks': validate_only_checks,
    'use_third_check': use_third_check,
    'type': journal_type,
  }
  return vals  

class account_journal_to_create(osv.osv_memory):
    
    _name = 'account.journal.to_create'

    global_type = [
      ('issue_check','Issue Check'),
      ('third_check','Third Check'),
      ('credit_card','Credit Card'),
      ('cash','Cash'),
      ('tax','Tax'),
      ('bank','Bank'),
      ]

    _columns = {
        'name': fields.char('Journal Name', size=64, required=True),
        'code': fields.char('Code', size=5, required=True, help="The code will be displayed on reports."),
        'account_id': fields.many2one('account.account', 'Account', required=True, domain=[('type','not in',['view','payable','receivable'])],),
        'config_id': fields.many2one('account.journal.config.wizard', 'Config',),
        'global_type': fields.selection(global_type, 'Global Type', required=True,),
        'update_posted': fields.boolean('Allow Cancelling', help="Check this box if you want to allow the cancellation the entries related to this journals or of the invoice related to this journals"),        
        'allow_date':fields.boolean('Date in Period', help= 'If checked, the entry won\'t be created if the entry date is not included into the selected period'),
        'direction': fields.selection([('in', 'In'),('out','Out')], 'Direction', size=32, required=False,
                                 help="Select 'In' for customer payments."\
                                 " Select 'Out' for supplier payments."),
        'use_issued_check': fields.boolean('Use Issued Checks', help='Allow to user Issued Checks in associated vouchers.'),
        'use_third_check': fields.boolean('Use Third Checks', help='Allow to user Third Checks in associated vouchers.'),
        'validate_only_checks': fields.boolean('Validate only Checks', help='If marked, when validating a voucher, verifies that the total amounth of the voucher is the same as the checks used.'),        
        'type': fields.selection([('sale', 'Sale'),('sale_refund','Sale Refund'), ('purchase', 'Purchase'), ('purchase_refund','Purchase Refund'), ('cash', 'Cash'), ('bank', 'Bank and Checks'), ('general', 'General'), ('situation', 'Opening/Closing Situation')], 'Type', size=32, required=True,
                                 help="Select 'Sale' for customer invoices journals."\
                                 " Select 'Purchase' for supplier invoices journals."\
                                 " Select 'Cash' or 'Bank' for journals that are used in customer or supplier payments."\
                                 " Select 'General' for miscellaneous operations journals."\
                                 " Select 'Opening/Closing Situation' for entries generated for new fiscal years."),        
        }

    _defaults= {
        'update_posted': True,
        'allow_date': True,
    }

# On change Functions
    def on_change_data(self, cr, uid, ids, account_id, global_type, force_change_global_type, context=None):
      # direction = False
      # direction, code = self.get_global_type_data(global_type)
      # Si global_type viene como false entonces get_journal_data se encarga de leerlo
      journal_data = {}
      if force_change_global_type:
        global_type = False
      if account_id:
        account = self.pool['account.account'].browse(cr, uid, account_id, context=context)
        name_sufix = context.get('name_sufix',False)
        name_prefix = context.get('name_prefix',False)
        code_sufix = context.get('code_sufix',False)
        point_of_sale = context.get('point_of_sale',0)
        journal_data = get_journal_data(point_of_sale, code_sufix, name_prefix, name_sufix, account, global_type)
      # if code_sufix:
      #   code += code_sufix 
      # code += '%%0%sd' % 2 % point_of_sale
      # return {'value':{'direction':direction, 'code':code}}
      return {'value':journal_data}

    def on_change_account(self, cr, uid, ids, account_id, context=None):
      # account_obj = self.pool['account.account']
      # value = {}
      # # name = ''
      # # name_sufix = context.get('name_sufix', False)
      # # name_prefix = context.get('name_prefix', False)
      # if account_id:
      #   account = account_obj.browse(cr, uid, account_id, context=context)
      #   global_type = self.get_global_type(cr, uid, account, context=context)
    
      # value['global_type'] = global_type
      # return {'value':value}
      return {}

    def create_journals(self, cr, uid, ids, wizard, context=None):
      account_journal_obj = self.pool['account.journal']
      for record in self.browse(cr, uid, ids, context=context):
        vals = {
          'name': record.name,
          'code': record.code,
          'direction': record.direction,
          'default_debit_account_id': record.account_id.id,
          'default_credit_account_id': record.account_id.id,
          'update_posted': record.update_posted,
          'allow_date': record.allow_date,
          'use_issued_check': record.use_issued_check,
          'validate_only_checks': record.validate_only_checks,
          'type': record.type,
        }
        account_journal_obj.create(cr, uid, vals, context=context)      

class account_journal_config_wizard(osv.osv_memory):
    
    _name = 'account.journal.config.wizard'

    _columns = {
        'code_sufix': fields.char('Code Sufix', size=2, required=True,),
        'name_sufix': fields.char('Name Sufix', size=16,),
        'name_prefix': fields.char('Name Prefix', size=16,),
        'company_id': fields.many2one('res.company', 'Company', required=True, readonly=True,),
        'remove_old_journals': fields.boolean('Eliminar los diarios existentes',
            help=u'Si es su primera instalación indique que necesita borrar los diarios existentes. Si agrega un nuevo punto de ventas indique que no va a eliminar los journals. Igual, puede indicar cuales borra y cuales no en el próximo paso.'),
        'point_of_sale': fields.integer(u'Número de Punto de Venta',
            help=u'Este es el número que aparecerá como prefijo del número de la factura. Si solo tiene un solo talonario ese número es 1. Si necesita agregar un nuevo punto de venta debe acceder a opciones Administración/Configuración/Wizards de Configuración/Wizards de Configuración y ejecutar nuevamente el wizard de "Configuración de Facturación".'),
        'account_ids': fields.many2many('account.account', 'account_journal_config_rel', 'config_id', 'account_id','Accounts', domain=[('type','not in',['view','payable','receivable'])],),
        'journals_to_remove_ids': fields.many2many('account.journal', 'journal_create_journal_to_remove_rel', 'config_id', 'journal_id', 'Journals to delete'),
        'journals_to_create_ids': fields.one2many('account.journal.to_create', 'config_id', 'Journals to Create'),
    }

    _defaults= {
        'company_id': lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, 'account.journal.config.wizard',context=c),
        'remove_old_journals': True,
        'point_of_sale': 1,
        'journals_to_create_ids': lambda self, cr, uid, c, context=None: self.update_create_journals(
            cr, uid, self.pool.get('res.company')._company_default_get(cr, uid, 'account.journal.config.wizard',context=c),context=c),
        'journals_to_remove_ids': lambda self, cr, uid, c, context=None: self.update_rem_journals(
            cr, uid, self.pool.get('res.company')._company_default_get(cr, uid, 'account.journal.config.wizard',context=c),context=c),
    }
        
    def get_suggested_accounts(self, cr, uid, company_id, context=None):
        """
        """
        journal_obj = self.pool.get('account.journal')
        account_obj = self.pool.get('account.account')
        
        # Get accounts of type liquidity
        liquidity_account_ids = account_obj.search(cr, uid, [
          ('type','in',['liquidity']),
          ('company_id','=',company_id)])

        # Get acash and bank journals
        journal_ids = journal_obj.search(cr, uid, [
          ('type','in',['bank','cash']),
          ('company_id','=',company_id)])

        # Get journals been removed
        remove_journal_ids = self.update_rem_journals(cr, uid, company_id, context=context)

        # Get active journals
        active_journal_ids = list(set(journal_ids) - set(remove_journal_ids))
        
        # Get active accounts from active journals
        active_account_ids = [journal.default_debit_account_id.id for journal in journal_obj.browse(cr, uid, active_journal_ids, context=context)]

        # Get liquidity accounts that are note been used
        new_liquidity_account_ids = list(set(liquidity_account_ids) - set(active_account_ids))

        return new_liquidity_account_ids

    def update_create_journals(self, cr, uid, company_id, context=None):
        """
        """
        point_of_sale = context.get('default_point_of_sale', False)
        code_sufix = context.get('default_code_sufix', False)
        name_prefix = context.get('default_name_prefix', False)
        name_sufix = context.get('default_name_sufix', False)

        ret = []
        account_obj = self.pool.get('account.account')
        account_ids = self.get_suggested_accounts(cr, uid, company_id, context=context)
        for account in account_obj.browse(cr, uid, account_ids, context=context):
          vals = get_journal_data(
            point_of_sale=point_of_sale, 
            code_sufix=code_sufix, 
            name_prefix=name_prefix, 
            name_sufix=name_sufix, 
            account=account)
          ret.append(vals)

        return ret 

    def confirm(self, cr, uid, ids, context=None):
        """
        Confirm Configure button
        """
        if context is None:
            context = {}

        for wzd in self.browse(cr, uid, ids, context=context):
          if wzd.remove_old_journals:
            self.delete_journals(cr, uid, wzd, context=context)
          self.pool['account.journal.to_create'].create_journals(cr, uid, [x.id for x in wzd.journals_to_create_ids], wzd, context=context)

    def delete_journals(self, cr, uid, wizard, context=None):
        """
        Delete all journals selected in journals_to_delete.
        """        
        for read in self.read(cr, uid, [wizard.id], ['journals_to_remove_ids']):
          self.pool['account.journal'].unlink(cr, uid, read['journals_to_remove_ids'], context=context)
        return     

    def update_rem_journals(self, cr, uid, company_id, context=None):
        """
        Remove Sale Journal, Purchase Journal, Sale Refund Journal, Purchase Refund Journal.
        """
        obj_journal = self.pool.get('account.journal')
        journal_ids = obj_journal.search(cr, uid, [
          ('type','in',['bank','cash']),
          ('company_id','=',company_id)])

        remove_journal_ids = []
        
        for journal_id in journal_ids:
          move_ids = self.pool['account.move'].search(cr, uid, [('journal_id','=',journal_id)], context=context)
          voucher_ids = self.pool['account.voucher'].search(cr, uid, [('journal_id','=',journal_id)], context=context)
          if not move_ids and not voucher_ids:
            remove_journal_ids.append(journal_id)

        return remove_journal_ids

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
