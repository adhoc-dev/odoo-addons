# -*- coding: utf-8 -*-
##############################################################################
#
#    Ingenieria ADHOC - ADHOC SA
#    https://launchpad.net/~ingenieria-adhoc
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.report import report_sxw
from openerp.report.report_sxw import rml_parse
import time
from openerp.tools.translate import _
import conversor
from openerp.osv import osv

class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        ret = super(Parser, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'logo_report': False,
            'partner_address': self.partner_address,
        })
        
        try:
            report_conf_id = int(name)
        except:
            title = _('Incorrect Configuration name')
            message = _('A number was expected for the report name but instead it was "%s".') % name
            raise osv.except_osv(title, message)
        
        report_conf_obj = self.pool.get('report_aeroo_generator.report_configuration')
        report_conf = report_conf_obj.browse(cr, uid, report_conf_id, context=context)
        if isinstance(report_conf, list):
            report_conf = report_conf[0]
        
        if not report_conf:
            title = _('No configuration object')
            message = _('There is no report defined for Invoices with this parameters of in general.')
            raise osv.except_osv(title, message)
        
        # We add all the key-value pairs of the report configuration
        for report_conf_line in report_conf.line_ids:
            if report_conf_line.value_type == 'text':
                self.localcontext.update({report_conf_line.name: report_conf_line.value_text})
            elif report_conf_line.value_type == 'boolean':
                self.localcontext.update({report_conf_line.name: report_conf_line.value_boolean})
        
        # We add the report configuration
        self.localcontext.update({'report_configuration': report_conf})
        
        # We add the company of the active object
        company_id = False
        if 'active_model' in context and 'active_id' in context:
            active_model_obj = self.pool.get(context['active_model'])
            active_object = active_model_obj.browse(cr, uid, context['active_id'], context=context)
            if hasattr(active_object, 'company_id') and active_object.company_id:
                self.localcontext.update({'company': active_object.company_id})
        
        # We add logo
        if report_conf.print_logo == 'specified_logo':
            self.localcontext.update({'logo_report': report_conf.logo})
        elif report_conf.print_logo == 'company_logo':
            if active_object.company_id.logo:
                self.localcontext.update({'logo_report': active_object.company_id.logo})
        else:
            self.localcontext.update({'logo_report': False})
        
        # We add background_image
        self.localcontext.update({'use_background_image': report_conf.use_background_image})
        if report_conf.use_background_image:
            self.localcontext.update({'background_image': report_conf.background_image})
        else:
            self.localcontext.update({'background_image': False})
        
        self.localcontext.update({
            'format_vat': self.format_vat,
            'address_from_partner': self.address_from_partner,
            'minus': self.minus,
            'number_to_string': self.number_to_string,
            'net_price': self.net_price,
            'price_unit_included_taxes': self.price_unit_included_taxes,
            'net_price_included_taxes': self.net_price_included_taxes,
            'price_subtotal_included_taxes': self.price_subtotal_included_taxes,
            'amount_untaxed_included_taxes': self.amount_untaxed_included_taxes,
            'get_to_discriminate_invoice_taxes': self.get_to_discriminate_invoice_taxes,
            'get_to_manual_invoice_taxes': self.get_to_manual_invoice_taxes,
            'get_base_invoice_taxes': self.get_base_invoice_taxes,
            'get_amount_invoice_taxes': self.get_amount_invoice_taxes,
            'get_main_partner': self.get_main_partner,
        })

    def get_main_partner(self, partner_id, context=None):
        if partner_id.parent_id:
            return partner_id.parent_id
        return partner_id

# Otras funciones genericas
    # Partner
    def partner_address(self, partner, context=None):
        ret = ''
        if partner.street:
            ret += partner.street
        if partner.street2:
            if partner.street:
                ret += ' - ' + partner.street2
            else:
                ret += partner.street2
        if ret != '':
            ret += '. '
        
        if partner.zip:
            ret += '(' + partner.zip + ')'
        if partner.city:
            if partner.zip:
                ret += ' ' + partner.city
            else:
                ret += partner.city
        if partner.state_id:
            if partner.city:
                ret += ' - ' + partner.state_id.name
            else:
                ret += partner.state_id.name
        if partner.zip or partner.city or partner.state_id:
            ret += '. '
        
        if partner.country_id:
            ret += partner.country_id.name + '.'
        
        return ret



    def format_vat(self, vat):
        formated_vat = False
        if vat and len(vat) > 2 and vat[0:2].lower() == "ar":
            vat_len = len(vat)
            formated_vat = '%s-%s-%s' % (vat[2:4], vat[4:vat_len-1], vat[vat_len-1:vat_len])
        return formated_vat
    
    def address_from_partner(self, partner):
        default_addr = False
        first_addr = False
        for address in partner.address:
            if address.type == 'invoice':
                return address
            elif address.type == 'default' and not default_addr:
                default_addr = address
        if default_addr:
            return default_addr
        elif partner.address:
            partner.address[0]
        else:
            return False
    
    def minus(self, val1, val2):
        return val1 - val2
    
    def number_to_string(self, val):
        return conversor.to_word(val)
    
    def net_price(self, gross_price, discount):
        return gross_price * (1-(discount / 100))
    
    # Functions for printing invoice data
    def price_unit_included_taxes(self, report_conf, invoice_line):
        '''
        Given a report configuration and an invoice line it returns the unit price of the invoice line,
        after applying the corresponding taxes, taking into consideration the once defined in the report configuration
        '''
        if not invoice_line:
            return None
        tax_not_to_discriminate, tax_to_discriminate = self.invoice_line_discriminate_taxes(report_conf, invoice_line)
        tax_not_to_discriminate = self.remove_included_taxes(tax_not_to_discriminate)
        return self.apply_taxes(tax_not_to_discriminate, invoice_line.price_unit)
    
    def net_price_included_taxes(self, report_conf, invoice_line):
        '''
        Given a report configuration and an invoice line it returns the net price of the invoice line,
        after applying the corresponding taxes, taking into consideration the once defined in the report configuration
        '''
        if not invoice_line:
            return None
        tax_not_to_discriminate, tax_to_discriminate = self.invoice_line_discriminate_taxes(report_conf, invoice_line)
        tax_not_to_discriminate = self.remove_included_taxes(tax_not_to_discriminate)
        return self.apply_taxes(tax_not_to_discriminate, self.net_price(invoice_line.price_unit, invoice_line.discount))
    
    def price_subtotal_included_taxes(self, report_conf, invoice_line):
        '''
        Given a report configuration and an invoice line it returns the subtotal price of the invoice line,
        after applying the corresponding taxes, taking into consideration the once defined in the report configuration
        '''
        if not invoice_line:
            return None
        tax_not_to_discriminate, tax_to_discriminate = self.invoice_line_discriminate_taxes(report_conf, invoice_line)
        return self.apply_taxes(tax_not_to_discriminate, invoice_line.price_subtotal)
    
    def amount_untaxed_included_taxes(self, report_conf, invoice):
        '''
        Given a report configuration and an invoice it returns the untaxed amount of the whole invoice,
        after applying the corresponding taxes that are defined in the invoice lines and not the one defined
        in the invoice.
        This takes into consideration the taxes defined in the report configuration
        '''
        if not invoice.invoice_line:
            return invoice.amount_untaxed
        
        tax_not_to_discriminate, tax_to_discriminate = self.invoice_discriminate_taxes(report_conf, invoice)
        return self.apply_taxes_to_invoice_lines(tax_not_to_discriminate, invoice.amount_untaxed, invoice)
    
    def get_to_discriminate_invoice_taxes(self, report_conf, invoice):
        '''
        This functions returns all the taxes associated to the invoice lines that should be shown discriminated
        in the last bottom of the invoice report.
        Return instances of account.tax
        '''
        if not invoice.invoice_line:
            return []
        
        tax_not_to_discriminate, tax_to_discriminate = self.invoice_discriminate_taxes(report_conf, invoice)
        return tax_to_discriminate
    
    def get_to_manual_invoice_taxes(self, report_conf, invoice):
        '''
        This functions returns all the manual taxes associated to the invoice, this taxes always are discriminated.
        Return instances of account.invoice.tax
        '''
        if not invoice.invoice_line:
            return []
        
        manual_tax_to_discriminate = []
        for tax in invoice.tax_line:
            if tax.manual:
                manual_tax_to_discriminate.append(tax)
        return manual_tax_to_discriminate
    
    def get_amount_invoice_taxes(self, report_conf, tax, invoice):
        amount = 0.0
        for line in invoice.invoice_line:
            if tax in line.invoice_line_tax_id:
                if tax.type == 'percent':
                    amount += tax.amount * line.price_subtotal
                elif tax.type == 'fixed':
                    amount += tax.amount
        return amount
    
    def get_base_invoice_taxes(self, report_conf, tax, invoice):
        base = 0.0
        for line in invoice.invoice_line:
            if tax in line.invoice_line_tax_id:
                base += line.price_subtotal
        return base
    
    def remove_included_taxes(self, tax_list):
        '''
        Given a tax_list (account.tax objects) it removes the taxes that have the field price_include to true
        '''
        new_tax_list = []
        for tax in tax_list:
            if not tax.price_include:
                new_tax_list.append(tax)
        return new_tax_list
        
    def apply_taxes(self, tax_list, quantity):
        '''
        Given a tax_list (account.tax objects) and a quantity it applies the taxes on the quantity
        '''
        if not tax_list:
            return quantity
        
        fix_taxes = 0.0
        per_taxes = 0.0
        for tax in tax_list:
            if tax.type and tax.amount:
                if tax.type == 'percent':
                    per_taxes += quantity * tax.amount
                elif tax.type == 'fixed':
                    fix_taxes += tax.amount
        quantity += per_taxes
        quantity += fix_taxes
        return quantity
    
    def apply_taxes_to_invoice_lines(self, tax_list, quantity, invoice):
        '''
        Given a tax_list (account.tax objects), a quantity and an invoice it applies the taxes on the quantity
        based on the definition of the invoice.
        '''
        if not tax_list:
            return quantity
        fix_taxes = 0.0
        per_taxes = 0.0
        for invoice_line in invoice.invoice_line:
            for tax in tax_list:
                if tax in invoice_line.invoice_line_tax_id:
                    if tax.type and tax.amount:
                        if tax.type == 'percent':
                            per_taxes += invoice_line.price_subtotal * tax.amount
                        elif tax.type == 'fixed':
                            fix_taxes += tax.amount
        quantity += per_taxes
        quantity += fix_taxes
        return quantity
    
    def invoice_line_discriminate_taxes(self, report_conf, invoice_line):
        '''
        Given a configuration report and an invoice line it returns the list of taxes that should be discriminated
        for that line and also the list of taxes that should not be discriminated.
        Return a list of objects of type account.tax
        '''
        if not report_conf or not invoice_line:
            return []
        if report_conf.type and report_conf.type == 'account.invoice' and report_conf.account_invoice_tax_included:
            tax_to_discriminate = []
            tax_not_to_discriminate = []
            for line_tax in invoice_line.invoice_line_tax_id:
                if line_tax in report_conf.account_invoice_tax_ids:
                    tax_not_to_discriminate.append(line_tax)
                else:
                    tax_to_discriminate.append(line_tax)
            return tax_not_to_discriminate, tax_to_discriminate
        else:
            tax_to_discriminate = []
            for line_tax in invoice_line.invoice_line_tax_id:
                tax_to_discriminate.append(line_tax)
            return [], tax_to_discriminate
    
    
    def invoice_discriminate_taxes(self, report_conf, invoice):
        '''
        Given a configuration report and an invoice it returns the list of taxes that should be discriminated
        for the lines of the invoice and also the list of taxes that should not be discriminated.
        Return a list of objects of type account.tax
        '''
        if not report_conf or not invoice:
            return []
        if report_conf.type and report_conf.type == 'account.invoice' and report_conf.account_invoice_tax_included:
            tax_to_discriminate = []
            tax_not_to_discriminate = []
            for invoice_line in invoice.invoice_line:
                for line_tax in invoice_line.invoice_line_tax_id:
                    if line_tax in report_conf.account_invoice_tax_ids:
                        if line_tax not in tax_not_to_discriminate:
                            tax_not_to_discriminate.append(line_tax)
                    else:
                        if line_tax not in tax_to_discriminate:
                            tax_to_discriminate.append(line_tax)
            return tax_not_to_discriminate, tax_to_discriminate
        else:
            tax_to_discriminate = []
            for invoice_line in invoice.invoice_line:
                for line_tax in invoice_line.invoice_line_tax_id:
                    if line_tax not in tax_to_discriminate:
                        tax_to_discriminate.append(line_tax)
            return [], tax_to_discriminate


