from openerp import api, fields, models


class res_partner(models.Model):
    _inherit = 'res.partner'

    # move_ids = fields.Many2many(
    #     compute='_get_moves',
    #     string='Moves'
    #     )

    # @api.multi
    # def _get_moves(self):
    #     for partner in self:
    #         partner.move_ids = partner.get_moves()

    # @api.multi
    # def get_moves(
    #         self, account_types, company_id=False):
    #     self.ensure_one()
    #     print 'context', self._context
    #     # TODO move this to the wizard
    #     if account_types == 'customer':
    #         types = ['receivable']
    #     elif account_types == 'supplier':
    #         types = ['payable']
    #     else:
    #         types = ['receivable', 'payable']

    #     moves_domain = [
    #         ('account_id.type', 'in', types),
    #         ('partner_id', '=', self.id),
    #         ]
    #     # TODO ver si el from date y el to date los filtramos a parte
    #     # if from_date:
    #         # moves_domain.append(('date', '=', company_id))
    #     if company_id:
    #         moves_domain.append(('company_id', '=', company_id))
    #     return self.env['account.move.line'].search(
    #         moves_domain).mapped('move_id').sorted(key=lambda r: r.date)
    #     # return self.mapped('')

    @api.model
    def get_account_types(self, result_selection):
        if result_selection == 'customer':
            types = "('receivable')"
        elif result_selection == 'supplier':
            types = "('payable')"
        else:
            types = "('payable', 'receivable')"
        return types

    @api.multi
    def get_summary_initial_balance(self):
        self.ensure_one()
        context = self._context
        from_date = context.get('from_date', False)
        company_id = context.get('company_id', False)
        result_selection = context.get('result_selection', False)
        account_types = self.get_account_types(result_selection)

        keys = ['debit', 'credit', 'balance']
        if not from_date:
            return dict(zip(keys, [0.0, 0.0, 0.0]))
        other_filters = " AND m.date < \'%s\'" % from_date
        if company_id:
            other_filters += " AND m.company_id = %i" % company_id

        query = """SELECT SUM(l.debit), SUM(l.credit), SUM(l.debit- l.credit)
            FROM account_move_line l
            LEFT JOIN account_account a ON (l.account_id=a.id)
            LEFT JOIN account_move m ON (l.move_id=m.id)
            WHERE a.type IN %s
            AND l.partner_id = %i
            %s
              """ % (account_types, self.id, other_filters)
        self._cr.execute(query)
        res = self._cr.fetchall()

        return dict(zip(keys, res[0]))

    @api.multi
    def get_summary_moves_data(self):
        self.ensure_one()

        context = self._context
        from_date = context.get('from_date', False)
        # time.localtime() (put in report or here
        to_date = context.get('to_date', False)
        company_id = context.get('company_id', False)
        result_selection = context.get('result_selection', False)
        account_types = self.get_account_types(result_selection)

        # aaaaaaa {'uid': 1, u'to_date': False, u'search_disable_custom_filters': True, 'print_id': 36284, 'lang': u'es_AR', u'active_ids': [222], 'tz': False, u'active_model': u'res.partner', u'show_invoice_detail': False, u'result_selection': u'customer_supplier', u'company_id': False, u'from_date': False, u'params': {u'action': 457}, 'aeroo_docs': True, u'show_receipt_detail': False, u'active_id': 222}
        other_filters = ""
        if from_date:
            other_filters += " AND m.date >= \'%s\'" % from_date
        if to_date:
            other_filters += " AND m.date <= \'%s\'" % to_date
        if company_id:
            other_filters += " AND m.company_id = %i" % company_id

        query = """SELECT l.move_id, l.date_maturity, SUM(l.debit), SUM(l.credit)
            FROM account_move_line l
            LEFT JOIN account_account a ON (l.account_id=a.id)
            LEFT JOIN account_move m ON (l.move_id=m.id)
            WHERE a.type IN %s
            AND l.partner_id = %i
            %s
            GROUP BY m.date, l.move_id, l.date_maturity
            ORDER BY m.date ASC, l.date_maturity DESC
              """ % (account_types, self.id, other_filters)
        self._cr.execute(query)
        res = self._cr.fetchall()

        lines_vals = []
        balance = 0.0
        for line in res:
            # print 'line[0]', line[0]
            debit = line[2]
            credit = line[3]
            balance += debit - credit
            lines_vals.append({
                'move': self.env['account.move'].browse(line[0]),
                'date_maturity': line[1],
                'debit': debit,
                'credit': credit,
                'balance': balance,
                })
        return lines_vals

# class account_move(models.Model):
#     _inherit = 'account.move'

#     @api.multi
#     def get_move_lines(
#             self, partner, from_date=False, to_date=False):
#         self.ensure_one()
#         self.env['account.move.line'].search([('')])
#         self.line_id.filtered(lambda x: x.type in types)
