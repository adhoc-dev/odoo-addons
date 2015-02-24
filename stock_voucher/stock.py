# -*- coding: utf-8 -*-
from openerp import fields, models, _, api
import openerp.addons.decimal_precision as dp


class stock_picking_type(models.Model):
    _inherit = "stock.picking.type"

    book_id = fields.Many2one(
        'stock.book', 'Book',
        help='Book suggested for pickings of this type',
        )
    # constraint de que el book y el type deben ser de la misma company_id


class stock_book(models.Model):
    _name = 'stock.book'
    _description = 'Stock Voucher Book'

    name = fields.Char(
        'Name', required=True,
        )
    sequence_id = fields.Many2one(
        'ir.sequence', 'Stock Voucher Sequence',
        domain=[('code', '=', 'stock.voucher')],
        context="{'default_code': 'stock.voucher', 'default_name': name, 'default_prefix': '000X-', 'default_padding': 8}",
        required=True,
        )
    lines_per_voucher = fields.Integer(
        'Lines Per Voucher', required=True,
        help="If voucher don't have a limit, then live 0. If not, this number will be used to calculate how many sequence are used on each picking"
        )
    company_id = fields.Many2one(
        'res.company', 'Company', required=True,
        default=lambda self: self.env[
            'res.company']._company_default_get('stock.book'),
        )


class stock_picking_voucher(models.Model):
    _name = 'stock.picking.voucher'
    _description = 'Stock Voucher Book'
    _rec_name = 'number'

    number = fields.Char(
        'Number', copy=False, required=True,
        )
    book_id = fields.Many2one(
        'stock.book', 'Voucher Book',
        required=True,
        )
    picking_id = fields.Many2one(
        'stock.picking', 'Picking', ondelete='cascade',
        required=True,
        )
    company_id = fields.Many2one(
        'res.company', 'Company', required=True,
        related='picking_id.company_id', readonly=True,
        )
    # constraint de que el book y el picking deben ser de la misma company

    _sql_constraints = [
        ('voucher_number_uniq', 'unique(number, book_id)',
            _('The field "Number" must be unique per book.'))]


class stock_picking(models.Model):
    _inherit = 'stock.picking'

    book_id = fields.Many2one(
        'stock.book', 'Voucher Book', copy=False, readonly=True,
        )
    voucher_ids = fields.One2many(
        'stock.picking.voucher', 'picking_id', 'Vouchers',
        copy=False, readonly=True,
        )
    declared_value = fields.Float(
        'Declared Value', digits=dp.get_precision('Account'),
        )
    observations = fields.Text('Observations')

    @api.multi
    def do_print_voucher(self):
        '''This function prints the voucher'''
        report = self.env['report'].get_action(self, 'stock_voucher.report')
        if self._context.get('keep_wizard_open', False):
            report['type'] = 'ir.actions.report_dont_close_xml'
        return report
