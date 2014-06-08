import time

from osv import osv
from osv import fields
import openerp
import pooler

try:
    import openerp.addons.web.common.http as openerpweb
except ImportError:
    import web.common.http as openerpweb

class Support(openerpweb.Controller):
    _cp_path = '/web_support'
    
    @openerpweb.jsonrequest
    def send_email(self, req, error, origin, prefix, db_name):
        context = req.session.eval_context(req.context)
        #registry = openerp.modules.registry.RegistryManager.get(req.session._db)
        #cr = registry.db.cursor()
        
        db, pool = pooler.get_db_and_pool(req.session._db)
        cr = db.cursor()
        
        mail_obj = pool.get('mail.message')
        return mail_obj.send_email_support(cr, req.session._uid, error, origin, prefix, db_name, context=context)
    
    @openerpweb.jsonrequest
    def get_support_contract_information(self, req):
        support_contract_obj = req.session.model('support.support_contract')
        context = req.session.eval_context(req.context)
        
        support_contract = support_contract_obj.search_read(context=context)
        
        if not support_contract:
            return {'correct': False}
        
        if isinstance(support_contract, list):
            support_contract = support_contract[0]
        
        return {'correct': True, 'support_contract': support_contract}




