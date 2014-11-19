from openerp import models, api, fields


class account_fiscal_position(models.Model):

    _inherit = 'account.fiscal.position'

    @api.v7
    def map_tax(self, cr, uid, fposition_id, taxes, context=None):
        result = super(account_fiscal_position, self).map_tax(
            cr, uid, fposition_id, taxes, context=context)
        if fposition_id:
            taxes_without_src_ids = [
                x.tax_dest_id.id for x in fposition_id.tax_ids if not x.tax_src_id]
            result = set(result) | set(taxes_without_src_ids)
        return list(result)

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
