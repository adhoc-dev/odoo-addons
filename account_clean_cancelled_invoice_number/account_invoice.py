# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp.osv import osv

class invoice(osv.osv):
    _inherit = 'account.invoice'

    def clean_internal_number(self, cr, uid, ids, context=None):
        # We also clean reference for compatibility with argentinian localization
        self.write(cr, uid, ids, {'internal_number':False,'afip_document_number':False}, context=context)