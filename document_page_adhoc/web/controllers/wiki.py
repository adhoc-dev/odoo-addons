
import base64

import cherrypy

import openobject
from openobject.tools import expose

from openerp.controllers import SecuredController


class WikiView(SecuredController):
    _cp_path = "/wiki/wiki"

    def get_attachment(self, **kwargs):
        attachments = openobject.rpc.RPCProxy('ir.attachment')
        file_name = kwargs.get('file').replace("'", '').strip()
        id = kwargs.get('id').strip()

        ids = attachments.search([('datas_fname', '=', file_name),
                                  ('res_model', '=', 'wiki.wiki'),
                                  ('res_id', '=', id)])

        res = attachments.read(ids, ['datas'])[0].get('datas')
        return res, file_name

    @expose(content_type='application/octet')
    def getImage(self, *kw, **kws):
        res, _ = self.get_attachment(**kws)
        return base64.decodestring(res)

    @expose(content_type='application/octet')
    def getfile(self, *kw, **kws):
        res, file_name = self.get_attachment(**kws)
        cherrypy.response.headers['Content-Disposition'] = 'filename="%s"' % (file_name,)
        return base64.decodestring(res)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
