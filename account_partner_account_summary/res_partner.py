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

    @api.multi
    def get_moves(
            self, account_types, company_id=False):
        self.ensure_one()
        print 'context', self._context
        # TODO move this to the wizard
        if account_types == 'customer':
            types = ['receivable']
        elif account_types == 'supplier':
            types = ['payable']
        else:
            types = ['receivable', 'payable']

        moves_domain = [
            ('account_id.type', 'in', types),
            ('partner_id', '=', self.id),
            ]
        # TODO ver si el from date y el to date los filtramos a parte
        # if from_date:
            # moves_domain.append(('date', '=', company_id))
        if company_id:
            moves_domain.append(('company_id', '=', company_id))
        return self.env['account.move.line'].search(
            moves_domain).mapped('move_id')
        # return self.mapped('')
