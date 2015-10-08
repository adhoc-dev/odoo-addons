# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
import logging
from openerp import pooler, SUPERUSER_ID
_logger = logging.getLogger(__name__)


def migrate(cr, version):
    _logger.info(
        'Running post migrate of account_check from version %s' % version)
    cr.execute(
        "update account_check set owner_name='/'")
    pool = pooler.get_pool(cr.dbname)
    compute_net_amounts(cr, pool)


def compute_net_amounts(cr, pool):
    voucher_obj = pool['account.voucher']
    voucher_ids = voucher_obj.search(
            cr, SUPERUSER_ID, [], {})
    _logger.info('Computing net amount for vouchers %s' % voucher_ids)
    voucher_obj._set_net_amount(
            cr, SUPERUSER_ID, voucher_ids, {})
