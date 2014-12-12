# -*- coding: utf-8 -*-
from openerp import models, api, fields
import logging

_logger = logging.getLogger(__name__)


class product_template(models.Model):
    _inherit = 'product.template'

    @api.one
    @api.depends('ean13')
    def _calculate_isbn(self):
        isbn = False
        if self.ean13:
            ean13 = self.ean13.replace(' ', '').replace('-', '')
            if len(ean13) == 13 and ean13[0:3] == '978':
                isbn = self.ean13[3:12]
                check_digit = self.calculate_control_digit_isbn(isbn)
                isbn += check_digit
        self.isbn = isbn

    def calculate_control_digit_isbn(self, str_partial_isbn):
        if not str_partial_isbn:
            return None
        if len(str_partial_isbn) != 9:
            return None
        try:
            int(str_partial_isbn)
        except:
            return None

        val = 0
        for i in range(len(str_partial_isbn)):
            val += int(str_partial_isbn[i]) * (int(i) + 1)
        if val % 11 == 10:
            ret = 'X'
        else:
            ret = str(val % 11)
        return ret

    isbn = fields.Char(
        compute='_calculate_isbn',
        string='ISBN',
        store=True)
