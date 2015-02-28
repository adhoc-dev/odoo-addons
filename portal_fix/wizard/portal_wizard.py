# -*- coding: utf-8 -*-
from openerp.osv import osv


class portal_wizard_user(osv.osv_memory):
    """
            """
    _inherit = "portal.wizard.user"

    def _create_user(self, cr, uid, wizard_user, context=None):
        if not context:
            context = {}
        context['default_company_id'] = wizard_user.partner_id.company_id
        context['default_company_ids'] = wizard_user.partner_id.company_id
        return super(portal_wizard_user, self)._create_user(
            cr, uid, wizard_user, context=context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
