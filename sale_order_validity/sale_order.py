from openerp import fields, models, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp.exceptions import Warning


class sale_order(models.Model):
    _inherit = "sale.order"

    @api.model
    def get_validity_date(self):
        validity_date = False
        validity_period = self.company_id.sale_order_validity_days
        if validity_period:
            validity_date = (datetime.today() + relativedelta(
                days=validity_period)).strftime('%Y-%m-%d')
        return validity_date

    validity_date = fields.Date(
        "Validity Date",
        help="Define date until when quotation is valid",
        readonly=True,
        default=get_validity_date,
        # TODO price_security that only some users can change this field
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        track_visibility='onchange')

    @api.one
    def action_wait(self):
        self.check_validity()
        return super(sale_order, self).action_wait()

    @api.one
    def check_validity(self):
        today_date = datetime.today().strftime('%Y-%m-%d')
        if self.validity_date and self.validity_date < today_date:
            raise Warning(_('You can not confirm this quoatation as it was valid until %s! Please Update Validity.') % (
                today_date))

    @api.one
    def update_prices_and_validity(self):
        self.update_prices()
        validity_date = self.get_validity_date()
        self.validity_date = validity_date
        return True
