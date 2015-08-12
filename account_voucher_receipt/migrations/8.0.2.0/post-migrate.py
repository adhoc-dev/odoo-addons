# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
import logging
_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """
    Migrations to replace this module by l10n_ar_account_voucher
    Setps:
        1. Update this module
        2. Uninstall this module
        3. Install l10n_ar_account_voucher
    """
    _logger.info(
        'Running migrations to replace module account_voucher_receipt'
        ' by l10n_ar_account_voucher')
    update_data_external_ids(cr)
    update_checkbook_fields_external_id(cr)
    update_voucher_fields_external_id(cr)


def update_data_external_ids(cr):
    _logger.info(
        "Update data ids to 'l10n_ar_account_voucher'")

    data_ids = [
        'sequence_customer_receipt_1',
        'sequence_supplier_receipt_1',
        'customer_receiptbook_1',
        'supplier_receiptbook_1',
        'customer_receiptbook_2',
        'supplier_receiptbook_2',
        ]

    cr.execute(
        """UPDATE ir_model_data set module='l10n_ar_account_voucher' where
        module='account_voucher_receipt' and name in %s""" % (
            str(tuple(data_ids))))


def update_checkbook_fields_external_id(cr):
    _logger.info(
        "Updating fields external id for receiptbook "
        "so you can uninstall this module'")
    field_prefix = 'field_account_voucher_receiptbook_'
    fields_sufixs = [
        'sequence', 'name', 'type', 'sequence_type', 'sequence_id',
        'company_id', 'manual_prefix', 'padding', 'active',
        'document_class_id']
    fields_with_prefix = []
    for field in fields_sufixs:
        fields_with_prefix.append("%s%s" % (field_prefix, field))

    _logger.info("Moving fields of account_voucher_receipt' if installed")

    # cr.execute(
    #     """DELETE FROM ir_model_data where
    #     module='account_voucher_receipt' and name in %s""" % (
    #         str(tuple(fields_with_prefix))))
    cr.execute(
        """UPDATE ir_model_data set module='l10n_ar_account_voucher' where
        module='account_voucher_receipt' and name in %s""" % (
            str(tuple(fields_with_prefix))))


def update_voucher_fields_external_id(cr):
    _logger.info(
        "Updating fields external id for voucher"
        "so you can uninstall this module'")
    field_prefix = 'field_account_voucher_'
    fields_sufixs = [
        'manual_sufix', 'force_number', 'receiptbook_id']
    fields_with_prefix = []
    for field in fields_sufixs:
        fields_with_prefix.append("%s%s" % (field_prefix, field))

    _logger.info("Moving fields of account_voucher_receipt' if installed")
    print '11111', fields_with_prefix
    print 'updateing', str(tuple(fields_with_prefix))
    cr.execute(
        """UPDATE ir_model_data set module='l10n_ar_account_voucher' where
        module='account_voucher_receipt' and name in %s""" % (
            str(tuple(fields_with_prefix))))
