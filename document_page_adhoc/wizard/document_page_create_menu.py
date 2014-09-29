# -*- coding: utf-8 -*-


from openerp import SUPERUSER_ID
from openerp.osv import fields, osv

class document_page_create_menu(osv.osv_memory):
    """ Create Menu """
    _name = "document.page.create.menu"
    _description = "Wizard Create Menu"

    _columns = {
        'menu_name': fields.char('Menu Name', size=256, required=True),
        'menu_parent_id': fields.many2one('ir.ui.menu', 'Parent Menu', required=True),
    }

    def default_get(self, cr, uid, fields, context=None):
        if context is None:
            context = {}
        res = super(document_page_create_menu,self).default_get(cr, uid, fields, context=context)
        page_id = context.get('active_id')
        obj_page = self.pool.get('document.page')
        page = obj_page.browse(cr, uid, page_id, context=context)
        res['menu_name'] = page.name
        return res

    def document_page_menu_create(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        obj_page = self.pool.get('document.page')
        obj_view = self.pool.get('ir.ui.view')
        obj_menu = self.pool.get('ir.ui.menu')
        obj_action = self.pool.get('ir.actions.act_window')
        page_id = context.get('active_id', False)
        page = obj_page.browse(cr, uid, page_id, context=context)

        datas = self.browse(cr, uid, ids, context=context)
        data = False
        if datas:
            data = datas[0]
        if not data:
            return {}
        value = {
            'name': 'Document Page',
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'document.page',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'inlineview',
        }
        value['domain'] = "[('parent_id','=',%d)]" % (page.id)
        value['res_id'] = page.id

        action_id = obj_action.create(cr, SUPERUSER_ID, value)
        # only the super user is allowed to create menu due to security rules on ir.values
        menu_id = obj_menu.create(cr, SUPERUSER_ID, {
                        'name': data.menu_name,
                        'parent_id':data.menu_parent_id.id,
                        'icon': 'STOCK_DIALOG_QUESTION',
                        'action': 'ir.actions.act_window,'+ str(action_id),
                        }, context)
        obj_page.write(cr, uid, [page_id], {'menu_id':menu_id})
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
