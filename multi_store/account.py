# -*- coding: utf-8 -*-
from openerp import models, fields


class account_journal(models.Model):
    _inherit = 'account.journal'

    store_ids = fields.Many2many(
        'res.store', 'res_store_journal_rel', 'journal_id', 'store_id',
        'Store', help="""Users that are not of this store, can see this\
        journals records but can not post or modify any entry on them.""")
