from openerp import api, fields, models


class account_summary_wizard(models.TransientModel):
    _name = 'account_summary_wizard'
    _description = 'Partner Account Summary Wizard'

    from_date = fields.Date('From')
    to_date = fields.Date('To')
    show_invoice_detail = fields.Boolean('Show Invoice Detail')
    show_receipt_detail = fields.Boolean('Show Receipt Detail')
    result_selection = fields.Selection(
        [('customer', 'Receivable Accounts'),
        ('supplier', 'Payable Accounts'),
        ('customer_supplier', 'Receivable and Payable Accounts')],
        "Account Type's", required=True, default='customer_supplier')

    @api.multi
    def account_summary(self):
        active_id = self._context.get('active_id', False)
        if not active_id:
            return False
        partner = self.env['res.partner'].browse(active_id)
        return self.env['report'].with_context(
            from_date=self.from_date,
            to_date=self.to_date,
            show_invoice_detail=self.show_invoice_detail,
            show_receipt_detail=self.show_receipt_detail,
            result_selection=self.result_selection).get_action(
            partner, 'report_account_summary')        
