## Odoo-Argentina

### HOW TO UPGRADE
#### 8.0 august 2015
on august 2015 we release several modifications on checks and other modules, to do this update you can follow this:

1 update module list on odoo interface
2 Update checks module `-i account_voucher_payline,account_journal_payment_subtype -u account_check --without-demo=all -d [database_name]`
3 desintall depreciated module `account_bank_voucher`
4 optionally install this new modules: `-i account_transfer,account_tax_settlement_withholding --without-demo=all -d [database_name]`

We have depreciated account_voucher_receipt, for those using argentinian localization may like to see odoo-argentina repo and update installing l10n_ar_account_voucher (see odoo-argentina changelog)