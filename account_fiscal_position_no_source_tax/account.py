from openerp import models, api, fields


class account_fiscal_position(models.Model):

    _inherit = 'account.fiscal.position'

    @api.v8     # noqa
    def map_tax(self, taxes):
        result = super(account_fiscal_position, self).map_tax(taxes)
        taxes_without_src_ids = [
            x.tax_dest_id.id for x in self.tax_ids if not x.tax_src_id]
        result += result.browse(taxes_without_src_ids)
        return result


class account_fiscal_position_tax(models.Model):
    _inherit = 'account.fiscal.position.tax'

    tax_src_id = fields.Many2one(required=False)
