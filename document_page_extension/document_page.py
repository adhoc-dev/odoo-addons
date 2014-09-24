# -*- coding: utf-8 -*-


from openerp.osv import fields, osv
from openerp.tools.translate import _
import difflib
from openerp import tools

class document_page(osv.osv):
    _inherit = "document.page"


    _columns = {
        'google_doc': fields.boolean('Use Google Doc?'),
        # 'google_doc': fields.selection([('document','Document'),('spreadsheet','Spreadsheet'),('presentation','Presentation'),('drawing','Drawing')], 'Google Doc'),
        'width': fields.char('Width', size=8, help="For example 1000px"),
        'height': fields.char('Height', size=8, help="For example 1000px"),
        'hide_title': fields.boolean('Hide Title?'), 
        # 'withou_margin': fields.boolean('Without Margin'), no lo uso porque deberia poner dos campos related para poder mostrar dos campos
        'url': fields.char('Document or Publication URL (content)'),
        'active': fields.boolean('Active', help="Used also for hidin content for common users, only reacheable by advanced search"),
        'show_document_link': fields.boolean('Show Document Link?', help="Show the link to the document on the bottom of the view"),
        'document_url': fields.char('Document url'),
    }
    _defaults = {
        'type':'content',
        'active': 1,
    }

    def google_doc_change(self, cr, uid, ids, width, height, url, context=None):
        res = {}
        if width and height and url:
            content = '<iframe src="' + url + '" width="' + width + '" height="' + height + '" frameborder="0"></iframe>'
            # TODO convertir a pdf como hace este doc_view_pdf <iframe src="https://docs.google.com/viewer?url=https://docs.google.com/document/d/125CJmmlBfy7UgfYuBAmb1_HSCuyz8NV133361KTK1SE/export?format%3Dpdf&amp;id=125CJmmlBfy7UgfYuBAmb1_HSCuyz8NV133361KTK1SE&amp;embedded=true" style="width:100%; height:860px;" frameborder="0"></iframe>
            res['value'] = {
                'content': content
            }
        return res    

    # def update_content(self, cr, uid, ids, context=None):
    #     #move_obj = self.pool.get("stock.move")
    #     for record in self.browse(cr, uid, ids, context=context):
    #         vals = {'content': record.google_doc}
    #         self.write(cr, uid, record.id, vals, context=context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
