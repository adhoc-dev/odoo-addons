# -*- coding: utf-8 -*-
from openerp import models, _
from openerp.exceptions import Warning


class sale_order(models.Model):
    _inherit = 'sale.order'

    def action_wait(self, cr, uid, ids, context=None):
        for o in self.browse(cr, uid, ids, context=context):
            if o.company_id.restrict_sales == 'yes':
                if o.partner_id.partner_state != 'approved':
                    raise Warning(
                        _('In %s you can not sell to an Unapprove partner') % (o.company_id.name))
            elif o.company_id.restrict_sales == 'amount_depends':
                if o.partner_id.partner_state != 'approved' and o.amount_total >= o.company_id.restrict_sales_amount:
                    raise Warning(_('In %s you can not sell to an Unapprove partner amounts greater than %.2f') % (
                        o.company_id.name, o.company_id.restrict_sales_amount))
        return super(sale_order, self).action_wait(
            cr, uid, ids, context=context)
