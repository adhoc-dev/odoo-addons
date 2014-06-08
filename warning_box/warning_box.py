from openerp.osv import osv, fields 
from openerp.tools.translate import _
from openerp import pooler

WARNING_TYPES = [('warning','Warning'),('info','Information'),('error','Error')]

class warning_box(osv.osv_memory): 
    _name = 'warning_box' 
    _description = 'warning_box' 
    _columns = {'type': fields.selection(WARNING_TYPES, string='Type', readonly=True), 
                'title': fields.char(string="Title", size=100, readonly=True), 
                'message': fields.text(string="Message", readonly=True), } 
    _req_name = 'title'

    def _get_view_id(self, cr, uid):
        res = self.pool.get('ir.model.data').get_object_reference(cr, uid, 
            'warning_box', 'warning_box_form')
        if res:
            return res[1]
        else:
            return False
    
    def message(self, cr, uid, id, context):
        message = self.browse(cr, uid, id)
        message_type = [t[1]for t in WARNING_TYPES if message.type == t[0]][0]
        res = {
            'name': '%s: %s' % (_(message_type), _(message.title)),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self._get_view_id(cr, uid),
            'res_model': 'warning_box',
            'domain': [],
            'context': context,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': message.id
        }
        return res
    
    def warning(self, cr, uid, title, message, context=None):
        id = self.create(cr, uid, {'title': title, 'message': message, 'type': 'warning'})
        res = self.message(cr, uid, id, context)
        return res
    
    def info(self, cr, uid, title, message, context=None):
        id = self.create(cr, uid, {'title': title, 'message': message, 'type': 'info'})
        res = self.message(cr, uid, id, context)
        return res
    
    def error(self, cr, uid, title, message, context=None):
        id = self.create(cr, uid, {'title': title, 'message': message, 'type': 'error'})
        res = self.message(cr, uid, id, context)
        return res