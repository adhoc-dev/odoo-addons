# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (C) 2012 OpenERP - Team de Localización Argentina.
# https://launchpad.net/~openerp-l10n-ar-localization
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
import logging

_logger = logging.getLogger(__name__)

_all_taxes = lambda x: True
_all_except_vat = lambda x: x.tax_code_id.parent_id.name != 'IVA'

class account_invoice_line(osv.osv):
    """
    En argentina como no se diferencian los impuestos en las facturas, excepto el IVA,
    agrego funciones que ignoran el iva solamente a la hora de imprimir los valores.

    En esta nueva versión se cambia las tres variables a una única función 'price_calc'
    que se reemplaza de la siguiente manera:

        'price_unit_vat_included'         -> price_calc(use_vat=True, quantity=1, discount=True)[id]
        'price_subtotal_vat_included'     -> price_calc(use_vat=True, discount=True)[id]
        'price_unit_not_vat_included'     -> price_calc(use_vat=False, quantity=1, discount=True)[id]
        'price_subtotal_not_vat_included' -> price_calc(use_vat=False, discount=True)[id]

    Y ahora puede imprimir sin descuento:

        price_calc(use_vat=True, quantity=1, discount=False)
    """

    _inherit = "account.invoice.line"

    def price_calc(self, cr, uid, ids, use_vat=True, tax_filter=None, quantity=None, discount=None, context=None):
        res = {}
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        _tax_filter = tax_filter or ( use_vat and _all_taxes ) or _all_except_vat
        for line in self.browse(cr, uid, ids):
            _quantity = quantity if quantity is not None else line.quantity
            _discount = discount if discount is not None else line.discount
            _price = line.price_unit * (1-(_discount or 0.0)/100.0)
            _tax_ids = filter(_tax_filter, line.invoice_line_tax_id)
            taxes = tax_obj.compute_all(cr, uid,
                                        _tax_ids, _price, _quantity,
                                        product=line.product_id,
                                        partner=line.invoice_id.partner_id)
            res[line.id] = taxes['total_included']
            if line.invoice_id:
                cur = line.invoice_id.currency_id
                res[line.id] = cur_obj.round(cr, uid, cur, res[line.id])
        return res

    def compute_all(self, cr, uid, ids, tax_filter=None, context=None):
        res = {}
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        _tax_filter = tax_filter
        for line in self.browse(cr, uid, ids):
            _quantity = line.quantity
            _discount = line.discount
            _price = line.price_unit * (1-(_discount or 0.0)/100.0)
            _tax_ids = filter(_tax_filter, line.invoice_line_tax_id)
            taxes = tax_obj.compute_all(cr, uid,
                                        _tax_ids, _price, _quantity,
                                        product=line.product_id,
                                        partner=line.invoice_id.partner_id)

            _round = (lambda x: cur_obj.round(cr, uid, line.invoice_id.currency_id, x)) if line.invoice_id else (lambda x: x)
            res[line.id] = {
                'amount_untaxed': _round(taxes['total']),
                'amount_tax': _round(taxes['total_included'])-_round(taxes['total']),
                'amount_total': _round(taxes['total_included']), 
                'taxes': taxes['taxes'],
            }
        return res.get(len(ids)==1 and ids[0], res)

account_invoice_line()

class account_invoice(osv.osv):
    _inherit = "account.invoice"

    def afip_validation(self, cr, uid, ids, context={}):
        obj_resp_class = self.pool.get('afip.responsability_relation')

        for invoice in self.browse(cr, uid, ids):
            # If parter is not in Argentina, ignore it.
            if invoice.partner_id.country_id.name != 'Argentina':
                continue

            # Partner responsability ?
            if isinstance(invoice.partner_id.responsability_id, orm.browse_null):
                raise osv.except_osv(_('No responsability'),
                                     _('Your partner have not afip responsability assigned. Assign one please.'))

            # Take responsability classes for this journal
            invoice_class = invoice.journal_id.journal_class_id.document_class_id
            resp_class_ids = obj_resp_class.search(cr, uid, [('document_class_id','=', invoice_class.id)])

            # You can emmit this document?
            resp_class = [ rc.issuer_id.code for rc in obj_resp_class.browse(cr, uid, resp_class_ids) ]
            if invoice.journal_id.company_id.partner_id.responsability_id.code not in resp_class:
                raise osv.except_osv(_('Invalid emisor'),
                                     _('Your responsability with AFIP dont let you generate this kind of document.'))

            # Partner can receive this document?
            resp_class = [ rc.receptor_id.code for rc in obj_resp_class.browse(cr, uid, resp_class_ids) ]
            if False and invoice.partner_id.responsability_id.code not in resp_class:
                raise osv.except_osv(_('Invalid receptor'),
                                     _('Your partner cant recive this document. Check AFIP responsability of the partner, or Journal Account of the invoice.'))

            # If Final Consumer have pay more than 1000$, you need more information to generate document.
            if invoice.partner_id.responsability_id.code == 'CF' and invoice.amount_total > 1000 and \
               (invoice.partner_id.document_type_id.code in [ None, 'Sigd' ] or invoice.partner_id.document_number is None):
                raise osv.except_osv(_('Partner without Identification for total invoices > $1000.-'),
                                     _('You must define valid document type and number for this Final Consumer.'))
        return True

    def compute_all(self, cr, uid, ids, line_filter=lambda line: True, tax_filter=lambda tax: True, context=None):
        res = {}
        for inv in self.browse(cr, uid, ids, context=context):
            amounts = []
            for line in inv.invoice_line:
                if line_filter(line):
                    amounts.append(line.compute_all(tax_filter=tax_filter, context=context))

            s = {
                 'amount_total': 0,
                 'amount_tax': 0,
                 'amount_untaxed': 0,
                 'taxes': [],
                }
            for amount in amounts:
                for key, value in amount.items():
                    s[key] = s.get(key, 0) + value

            res[inv.id] = s

        return res.get(len(ids)==1 and ids[0], res)

    def onchange_partner_id(self, cr, uid, ids, type, partner_id,
                            date_invoice=False, payment_term=False,
                            partner_bank_id=False, company_id=False):
        result = super(account_invoice,self).onchange_partner_id(cr, uid, ids,
                       type, partner_id, date_invoice, payment_term,
                       partner_bank_id, company_id)

        if company_id and partner_id:
            # Set list of valid journals by partner responsability
            partner_obj = self.pool.get('res.partner')
            company_obj = self.pool.get('res.company')
            partner = partner_obj.browse(cr, uid, partner_id)
            company = company_obj.browse(cr, uid, company_id)
            responsability = partner.responsability_id
            if responsability.issuer_relation_ids is None:
                return result

            document_class_set = set([ i.document_class_id.id for i in responsability.issuer_relation_ids ])

            type_map = {
                'out_invoice': ['sale'],
                'out_refund': ['sale_refund'],
                'in_invoice': ['purchase'],
                'in_refund': ['purchase_refund'],
            }

            if not company.partner_id:
                result['warning']={'title': _('Your company has not setted any partner'),
                                   'message': _('That\'s is really strange. You must have a partner associated to your company.')}
                _logger.warning('Your company "%s" has not setted any partner.' % company.name)
                return result

            if not company.partner_id.responsability_id.id:
                result['warning']={'title': _('Your company has not setted any responsability'),
                                   'message': _('Please, set your company responsability in the company partner before continue.')}
                _logger.warning('Your company "%s" has not setted any responsability.' % company.name)
                return result

            cr.execute("""
                       SELECT DISTINCT J.id, J.name, IRSEQ.number_next
                       FROM account_journal J
                       LEFT join ir_sequence IRSEQ on (J.sequence_id = IRSEQ.id)
                       LEFT join afip_journal_class JC on (J.journal_class_id = JC.id)
                       LEFT join afip_document_class DC on (JC.document_class_id = DC.id)
                       LEFT join afip_responsability_relation RR on (DC.id = RR.document_class_id)
                       WHERE
                       (RR.id is Null OR (RR.id is not Null AND RR.issuer_id = %s AND RR.receptor_id = %s)) AND
                       J.type in %s AND                        
                       J.id is not NULL AND
                       J.sequence_id is not NULL
                       AND IRSEQ.number_next is not NULL
                       ORDER BY IRSEQ.number_next DESC;
                      """, (company.partner_id.responsability_id.id, partner.responsability_id.id, tuple(type_map[type])))
            accepted_journal_ids = [ x[0] for x in cr.fetchall() ]

            if 'domain' not in result: result['domain'] = {}
            if 'value' not in result: result['value'] = {}

            if accepted_journal_ids:
                result['domain'].update({
                    'journal_id': [('id','in', accepted_journal_ids)],
                })
                result['value'].update({
                    'journal_id': accepted_journal_ids[0],
                })
            else:
                result['domain'].update({
                    'journal_id': [('id','in',[])],
                })
                result['value'].update({
                    'journal_id': False,
                })

        return result

account_invoice()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

