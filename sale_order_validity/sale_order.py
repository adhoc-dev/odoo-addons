from openerp.osv import fields, osv

class sale_order(osv.osv):
    _inherit = "sale.order"

    _columns = {
            'validity_date': fields.date("Validity Date",
                                             help="Define date until when quotation is valid",
                                             readonly=True,
                                             # Todo in price_security that only some users can change this field manually
                                             states={
                                                 'draft': [('readonly', False)],
                                                 'sent': [('readonly', False)],
                                             },                                             
                                             track_visibility='onchange'),
            }
