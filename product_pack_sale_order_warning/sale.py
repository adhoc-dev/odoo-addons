#    Ingenieria ADHOC - ADHOC SA
#    https://launchpad.net/~ingenieria-adhoc


from openerp.osv import fields, osv
from openerp.tools import float_compare
from openerp.tools.translate import _

class sale_order_line(osv.osv):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'
    
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
        
        ret = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty=qty,
                    uom=uom, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
                    lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging, fiscal_position=fiscal_position,
                    flag=flag, context=context)
        
        if not product:
            return ret
        
        product_obj = self.pool.get('product.product')
        prod = product_obj.browse(cr, uid, product, context=context)
            
        if prod.stock_depends:
            warning_msgs = ret.get('warning') and ret['warning'].get('message') or ''
            warning_title = ret.get('warning') and ret['warning'].get('title') or _('Configuration Error !')
            
            if prod:
                warning_msgs += self.check_recursive_product_availability(cr, uid, prod, qty=qty, uom=uom, context=context)
            warning = {}
            
            if warning_msgs:
                warning = {'title': warning_title, 'message' : warning_msgs }
            ret['warning'] = warning
        
        return ret
    
    def check_recursive_product_availability(self, cr, uid, product, qty=0, uom=False, context=None):
        warning_msgs = ''
        if product.stock_depends:
            for pack_line in product.pack_line_ids:
                new_qty = qty * pack_line.quantity
                warning_msgs += self.check_recursive_product_availability(cr, uid, pack_line.product_id, qty=new_qty, uom=uom, context=context)
        else:
            warning_msgs += self.check_product_availability(cr, uid, product, qty=qty, uom=uom, context=context)
        
        return warning_msgs
        
    def check_product_availability(self, cr, uid, product, qty=0, uom=False, context=None):
        product_uom_obj = self.pool.get('product.uom')
        product_obj = self.pool.get('product.product')
        
        uom2 = False
        if uom:
            uom2 = product_uom_obj.browse(cr, uid, uom, context=context)
            if product.uom_id.category_id.id != uom2.category_id.id or context.get('force_product_uom'):
                uom = False
                uom2 = False
        
        if not uom2:
            uom2 = product.uom_id
        compare_qty = float_compare(product.virtual_available * uom2.factor, qty * product.uom_id.factor, precision_rounding=product.uom_id.rounding)
        
        warning_msgs = ''
        
        if (product.type == 'product') and int(compare_qty) == -1  and (product.procure_method == 'make_to_stock'):
            warn_msg = _('You plan to sell %.2f %s of %s but you only have %.2f %s available !\nThe real stock of %s is %.2f %s. (without reservations)') % \
                    (qty, uom2 and uom2.name or product.uom_id.name,
                     product.name,
                     max(0,product.virtual_available), product.uom_id.name,
                     product.name,
                     max(0,product.qty_available), product.uom_id.name)
            warning_msgs += _("Not enough stock ! : ") + warn_msg + "\n\n"
        
        return warning_msgs


sale_order_line()



