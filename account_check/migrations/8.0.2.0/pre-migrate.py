# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
import logging
_logger = logging.getLogger(__name__)


def migrate(cr, version):
    _logger.info('Migrating account_check from version %s' % version)
    cr.execute(
        "update account_check set type='issue_check' where type='issue'")
    cr.execute(
        "update account_check set type='third_check' where type='third'")
    cr.execute(
        "update account_journal set payment_subtype='third_check' where check_type='third'")
    cr.execute(
        "update account_journal set payment_subtype='issue_check' where check_type='issue'")
