# -*- coding: utf-8 -*-
{
    'name': 'Partner Credit Limit',
    'version': '1.0',
    'description': """Partner Credit Limit
    When approving a Sale Order it computes the sum of:
        * The credit the Partner has to paid
        * The amount of Sale Orders aproved but not yet invoiced
        * The invoices that are in draft state
        * The amount of the Sale Order to be aproved
    and compares it with the credit limit of the partner. If the
    credit limit is less it does not allow to approve the Sale
    Order""",
    'author': 'ADHOC SA',
    'website': 'www.ingadhoc.com',
    'depends': ['sale'],
    'data': [
        'security/partner_credit_limit_security.xml',
        'partner_view.xml',
        ],
    'demo': [],
    'test': [],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
