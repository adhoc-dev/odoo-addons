# -*- coding: utf-8 -*-


from openerp.osv import fields, osv
from openerp.tools.translate import _
import base64

class showdiff(osv.osv_memory):
    """ Disp[ay Difference for History """

    _name = 'wizard.document.page.history.show_diff'

    def get_diff(self, cr, uid, context=None):
        if context is None:
            context = {}
        history = self.pool.get('document.page.history')
        ids = context.get('active_ids', [])

        diff = ""
        if len(ids) == 2:
            if ids[0] > ids[1]:
                diff = history.getDiff(cr, uid, ids[1], ids[0])
            else:
                diff = history.getDiff(cr, uid, ids[0], ids[1])

        elif len(ids) == 1:
            old = history.browse(cr, uid, ids[0])
            nids = history.search(cr, uid, [('page_id', '=', old.page_id.id)])
            nids.sort()
            diff = history.getDiff(cr, uid, ids[0], nids[-1])
        else:
            raise osv.except_osv(_('Warning!'), _('You need to select minimum one or maximum two history revisions!'))
        return diff

    _columns = {
        'diff': fields.text('Diff', readonly=True),
    }

    _defaults = {
        'diff': get_diff
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
