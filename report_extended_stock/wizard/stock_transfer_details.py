# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp import fields, api, _
from openerp.exceptions import Warning


class stock_transfer_details(osv.osv_memory):

    _inherit = "stock.transfer_details"

    def _get_report(self, picking_id):
        return self.pool['ir.actions.report.xml'].get_report(
            self.env.cr, self.env.uid,
            'stock.picking', picking_id, self.env.context)

    def _get_max_lines(self):
        picking_id = self.env.context.get('active_id', False)
        ret = False
        if picking_id:
            report = self._get_report(picking_id)
            if report.stock_picking_split_picking_type_out:
                ret = report.stock_picking_lines_to_split
        return ret

    def _get_allow_dont_split(self):
        picking_id = self.env.context.get('active_id', False)
        ret = False
        if picking_id:
            report = self._get_report(picking_id)
            if report.stock_picking_split_picking_type_out:
                ret = report.stock_picking_dont_split_option
        return ret

    @api.one
    @api.depends('item_ids', 'max_lines')
    def get_excess_lines(self):
        excess_lines = False
        items_nbr = len(self.item_ids)
        if self.max_lines and items_nbr >= self.max_lines:
            excess_lines = items_nbr - self.max_lines
        self.excess_lines = excess_lines

    @api.one
    def do_detailed_transfer(self):
        if self.excess_lines > 0:
            msg = 'You can validate at most %s lines. \
            Try validating some of them and the validate the remaining moves.' % (self.max_lines)
            raise Warning(_(msg))
        else:
            return super(stock_transfer_details, self).do_detailed_transfer()

    excess_lines = fields.Integer(
        string='Excess Lines',
        compute='get_excess_lines',
        readonly=True)
    max_lines = fields.Integer(
        string='Maximum number of lines',
        help='Maximum number of lines allowed by the report',
        default=_get_max_lines,
        readonly=True)
    allow_dont_split = fields.Boolean(
        string='Allow Dont Split',
        default=_get_allow_dont_split,
        readonly=True)
    remove_excess_lines = fields.Boolean(
        string='Remove Excess Lines')
    dont_split = fields.Boolean(
        string="Don't Split")

    def onchange_remove_excess_lines(
            self, cr, uid, ids, remove_excess_lines,
            max_lines, item_ids, context=None):
        if context is None:
            context = {}
        ret = {}
        defaults = self.default_get(cr, uid, ['item_ids'], context=context)
        item_ids = defaults.get('item_ids', False)
        if item_ids:
            aux = []
            aux.append([5, False, False])
            for record in item_ids:
                aux.append([0, False, record])
            ret = {'value':
                   {'item_ids': aux
                    }
                   }
        if remove_excess_lines:
            ret = {'value':
                   {'item_ids': aux[:max_lines + 1]
                    }
                   }
        else:
            ret = {'value':
                   {'item_ids': aux
                    }
                   }
        return ret

    def onchange_dont_split(
            self, cr, uid, ids,
            dont_split, item_ids, context=None):
        if context is None:
            context = {}
        ret = {}
        if dont_split:
            ret['warning'] = {'title': "Warning!", 'message':
                              "With don't split option you can process the picking with exceeded lines.\nBut later, if you need to print the picking report, it wont fit in one page!\nPlease consider it carefully!"}
        return ret
