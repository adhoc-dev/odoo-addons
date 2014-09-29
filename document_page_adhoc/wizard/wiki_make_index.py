# -*- coding: utf-8 -*-


from osv import fields, osv
from tools.translate import _

class wiki_make_index(osv.osv_memory):
    """ Create Index For Selected Page """

    _name = "wiki.make.index"
    _description = "Create Index"

    def wiki_do_index(self, cr, uid, ids, context=None):

        """ Makes Index according to page hierarchy
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: list of wiki index’s IDs

        """
        if context is None:
            context = {}
        data = context and context.get('active_ids', []) or []
        
        if not data:
            return {'type':  'ir.actions.act_window_close'}
        
        for index_obj in self.browse(cr, uid, ids, context=context):
            wiki_pool = self.pool.get('wiki.wiki')
            cr.execute("Select id, section from wiki_wiki where id IN %s \
                            order by section ", (tuple(data),))
            lst0 = cr.fetchall()
            if not lst0[0][1]:
                raise osv.except_osv(_('Warning!'), _('There is no section in this Page.'))

            lst = []
            s_ids = {}

            for l in lst0:
                s_ids[l[1]] = l[0]
                lst.append(l[1])

            lst.sort()
            val = None
            def toint(x):
                try:
                    return int(x)
                except:
                    return 1

            lst = map(lambda x: map(toint, x.split('.')), lst)

            result = []
            current = ['0']
            current2 = []

            for l in lst:
                for pos in range(len(l)):
                    if pos >= len(current):
                        current.append('1')
                        continue
                    if (pos == len(l) - 1) or (pos >= len(current2)) or (toint(l[pos]) > toint(current2[pos])):
                        current[pos] = str(toint(current[pos]) + 1)
                        current = current[:pos + 1]
                        if pos == len(l) - 1:
                            break
                key = ('.'.join([str(x) for x in l]))
                id = s_ids[key]
                val = ('.'.join([str(x) for x in current[:]]), id)

            if val:
                result.append(val)
            current2 = l

            for rs in result:
                wiki_pool.write(cr, uid, [rs[1]], {'section':rs[0]})

        return {'type':  'ir.actions.act_window_close'}

wiki_make_index()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
