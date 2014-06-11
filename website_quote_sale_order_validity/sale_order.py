# -*- coding: utf-8 -*-
##############################################################################
#
#    Ingenieria ADHOC - ADHOC SA
#    https://launchpad.net/~ingenieria-adhoc
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import fields, osv
from datetime import time, datetime
from openerp.tools.translate import _
from ast import literal_eval
from dateutil.relativedelta import relativedelta


class sale_order(osv.osv):
    _inherit = "sale.order"

    _columns = {
            'validity_date': fields.date("Valid Until",
                                             help="Define date until when quotation is valid",
                                             readonly=True,
                                             # Todo in price_security that only some users can change this field manually
                                             states={
                                                 'draft': [('readonly', False)],
                                                 'sent': [('readonly', False)],
                                             },                                             
                                             track_visibility='onchange'),
            }

    def get_validity_date(self, cr, uid, context=None):
        company_id = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.id
        company_obj = self.pool.get('res.company')
        company_rec = company_obj.browse(cr, uid, company_id, context=context)
        validity_period = False
        validity_date = False
        if company_rec:
            validity_period = company_rec.sale_order_validity_days
        if validity_period and validity_period > 0:
            validity_date = (datetime.today() + relativedelta(days=validity_period)).strftime('%Y-%m-%d')
        return validity_date

    _defaults = {
        'validity_date': get_validity_date,
    }    

    def update_prices_and_validity(self, cr, uid, ids, context=None):
        if context == None:
            context = {}
        self.update_prices(cr, uid, ids, context=context)
        validity_date = self.get_validity_date(cr, uid, context=context)
        vals = {'validity_date':validity_date}
        self.write(cr, uid, ids, vals, context=context)
        return True

    def check_validity(self, cr, uid, ids):
        """ Tests whether state of move is cancelled or not.
        @return: True or False
        """
        for record in self.browse(cr, uid, ids):
            today_date = datetime.today().strftime('%Y-%m-%d')
            if record.validity_date and record.validity_date < today_date:
                raise osv.except_osv(_('Error in the validity!'), _('This quoatation was valid until %s!') % (today_date))
        return True        

