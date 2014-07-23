# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Mentis d.o.o.
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

from osv import fields, osv
from tools.translate import _
from datetime import datetime
import time

class account_interests(osv.osv_memory):
    _name = "account.interests"
    _description = "Calculate interests for selected partners"
    _columns = {
        'date_from': fields.date('Date from', required=True),
        'date_to': fields.date('Date to', required=True),
		'interest_rate': fields.float('Interest rate', digits=(2,2), required=True),
        'invoice_over_value': fields.float('Create invoice if interests are greater than', digits=(2,2), required=True),
        
    }
    _defaults = {
		'date_from': lambda *a: time.strftime('%Y-%m-01'),
        'date_to': lambda *a: time.strftime('%Y-%m-%d'),
        'interest_rate': lambda *a: 8.75,
        'invoice_over_value': lambda *a: 5,
	}
    
    def _prepare_invoice(self, cr, uid, partner_id, journal_id, context=None):
        
        partner = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)
        user = self.pool.get('res.users').browse(cr, uid, uid)
        
        #account_id = partner.property_account_receivable.id
        #payment_term = partner.property_payment_term.id or False
        
        invoice_vals = {
            'name': '',
            'origin': '',
            'type': 'out_invoice',
            'account_id': 198, #code - 120200
            'partner_id': partner.id,
            'comment': '',
            #'payment_term': payment_term,
            'fiscal_position': partner.property_account_position.id,
            'date_invoice': time.strftime('%Y-%m-%d'),
            'date_due': time.strftime('%Y-%m-%d'),
            'company_id': user.company_id.id,
            'user_id': uid,
            'journal_id': journal_id,
        }
        #invoice_vals['currency_id'] = cur_id
        return invoice_vals
    
    def _prepare_account_id(self, cr, uid, account_code, context=None):
        account_obj = self.pool.get('account.account')
        account_id = account_obj.search(cr, uid, [('code', '=', account_code)])
        return account_id[0]
    
    def _prepare_analytic_account_id(self, cr, uid, move_id, context=None):
        account_move_line_obj = self.pool.get('account.move.line')
        move_line_ids =  account_move_line_obj.search(cr, uid, [
                                                   ('move_id', '=', move_id),
                                                   ('analytic_account_id', '!=', None)
                                                   ], limit = 1)
        
        for line in account_move_line_obj.browse(cr, uid, move_line_ids):
            if line.analytic_account_id:
                return line.analytic_account_id.id
        
        return False
    
    def _prepare_description(self, cr, uid, invoice, date_start, date_end, saldo, interest_rate, context=None):
        date_diff = datetime.strptime(date_end,'%Y-%m-%d')  - datetime.strptime(date_start,'%Y-%m-%d')
        
        tmp_date_from = datetime.strptime(date_start, '%Y-%m-%d')
        tmp_date_from = tmp_date_from.strftime('%d-%m-%Y')
        tmp_date_to = datetime.strptime(date_end, '%Y-%m-%d')
        tmp_date_to = tmp_date_to.strftime('%d-%m-%Y')
        
        if invoice.journal_id.id == 15: #prenos starih racunov
            if invoice.ref:
                if invoice.ref == 'OTV-SK-2013':
                    naziv = invoice.name
                else:
                    naziv = invoice.ref
            else:
                if invoice.name and invoice.name != '':
                    naziv = invoice.name
                else:
                    naziv = '_'
                    
        else:
            naziv = invoice.move_id.name #Preberemo iz account_move


        comment = 'IFA: ' + naziv.replace(',', ' ') + ', '
        comment += 'Od dne: ' + tmp_date_from + ', '
        comment += 'Do dne: ' + tmp_date_to + ', '
        comment += 'Dni: ' + str(date_diff.days) + ', '
        comment += 'Glavnica(eur): ' + str(saldo) + ', '
        comment += 'Obr.mera(%): ' + str(interest_rate)
        
        return comment
            
            
    def calc_interests(self, cr, uid, dt_from, dt_to, saldo, in_rate):
        #1. Izracunamo cas med koncnim in zacetnim datumom
        date_diff = datetime.strptime(dt_to,'%Y-%m-%d')  - datetime.strptime(dt_from,'%Y-%m-%d')
        #2. Kalkulacija
        interest_procent = in_rate / 100
        interest_days = float(date_diff.days) / 365
        return interest_days * interest_procent * saldo
    
    
    def calculate(self, cr, uid, ids, context=None):

        if context is None:
            context = {}
        active_ids = context.get('active_ids',[])
        
        date_from = self.browse(cr,uid,ids)[0].date_from
        date_to = self.browse(cr,uid,ids)[0].date_to
        interest_rate = self.browse(cr,uid,ids)[0].interest_rate
        limit_value = self.browse(cr,uid,ids)[0].invoice_over_value
        
        if date_to <= date_from:
            raise osv.except_osv(_('Warning!'), _('Date to cannot be lower or equal to Date from.'))
        
        journal_id = [1,3,15]  #Izdane fakture, Izdani dobropisi, Temeljnica-prenos prometa kupci
        account_id = ['120000', '120100'] #Kratkorocne terjatve do kupcev v drzavi / v tujini
        
        #partner_obj = self.pool.get('res.partner')
        invoice_obj = self.pool.get('account.invoice')
        invoice_line_obj = self.pool.get('account.invoice.line')
        
        for partner_id in active_ids:
            
            postavke = {}
            interest = 0
            account_move_line_obj = self.pool.get('account.move.line')
            move_line_ids =  account_move_line_obj.search(cr, uid, [
                                                   ('partner_id', '=', partner_id),
                                                   ('journal_id', 'in', journal_id),
                                                   ('account_id.code', 'in', account_id),
                                                   ('date_maturity', '<', date_to)
                                                   ], order='date_maturity')
            
            #0. Se sprehajamo po racunih stranke
            for line in account_move_line_obj.browse(cr, uid, move_line_ids):
                
                #1.kateri zacetni datum jemljemo
                if line.date_maturity < date_from:
                    date_start = date_from
                else:
                    date_start = line.date_maturity
                    
                saldo = line.debit
                
                #2. Ze bilo delno ali polno placilo
                if line.reconcile:
                    
                    move_line_all_ids =  account_move_line_obj.search(cr, uid, ['|',
                                                                                ('reconcile_id.name', '=', line.reconcile),
                                                                                ('reconcile_partial_id.name', '=', line.reconcile),
                                                                                ('id', '!=', line.id),
                                                                                ('date', '<', date_to),
                                                                                ], order='date')
                    #2. Gledamo vsa placila za ta racun - vse linije z istim reconsilom
                    for line_all in account_move_line_obj.browse(cr, uid, move_line_all_ids):
                        
                        #2.1 Preverimo ali je bilo placilo izvedeno pred date_start, potem ga odstejemo od debita
                        if line_all.date <= date_start:
                            saldo -= line_all.credit
                        else:
                            interest_res = self.calc_interests(cr, uid, date_start, line_all.date, saldo, interest_rate)
                            
                            comment = self._prepare_description(cr, uid, line, date_start, line_all.date, saldo, interest_rate)
                            postavke[len(postavke)] = [comment, round(interest_res,2), line.move_id.id]
                            
                            interest += interest_res
                            saldo -= line_all.credit
                            date_start = line_all.date
                    
                    if round(saldo,2) > 0: #ni vec placil, torej obresti do koncnega datuma
                        interest_res = self.calc_interests(cr, uid, date_start, date_to, saldo, interest_rate)
                        comment = self._prepare_description(cr, uid, line, date_start, date_to, saldo, interest_rate)
                        postavke[len(postavke)] = [comment, round(interest_res,2), line.move_id.id]
                        interest += interest_res
                    
                    
                #3. Se sploh ni bilo placano 
                else: 
                    interest_res = self.calc_interests(cr, uid, date_start, date_to, saldo, interest_rate)
                    comment = self._prepare_description(cr, uid, line, date_start, date_to, saldo, interest_rate)
                    postavke[len(postavke)] = [comment, round(interest_res,2), line.move_id.id]
                    interest += interest_res
                    
                
            #4. Konec enega racuna - mam zbrane postavke, samo racun se naredim
            if postavke and round(interest,2) >= limit_value:
                #Priprava Racuna
                invoice_vals = self._prepare_invoice(cr, uid, partner_id, 2)
                tmp_date_from = datetime.strptime(date_from, '%Y-%m-%d')
                tmp_date_from = tmp_date_from.strftime('%d-%m-%Y')
                
                tmp_date_to = datetime.strptime(date_to, '%Y-%m-%d')
                tmp_date_to = tmp_date_to.strftime('%d-%m-%Y')
                
                invoice_vals['comment'] = 'Obračun zamudnih obresti za obdobje med ' + tmp_date_from + ' in ' + tmp_date_to
                inv_id = invoice_obj.create(cr, uid, invoice_vals)
                
                #Priprava postavk
                for pos in postavke:
                    if postavke[pos][1] > 0:
                        analytic_id = self._prepare_analytic_account_id(cr, uid, postavke[pos][2], context)
                        invoice_line_obj.create(cr, uid, {
                                                          'name': postavke[pos][0],
                                                          'origin': '',
                                                          'invoice_id': inv_id,
                                                          'account_id': self._prepare_account_id(cr, uid, '777000', context),
                                                          'account_analytic_id': analytic_id,
                                                          'price_unit': postavke[pos][1],
                                                          'quantity': 1 
                                                          })
        
        return {
                'type': 'ir.actions.act_window_close',
        }
    
account_interests()

