# -*- coding: utf-8 -*-
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from openerp import models
from openerp.exceptions import except_orm
from openerp.tools.translate import _
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT


class partner(models.Model):

    """"""

    _inherit = 'res.partner'

    _columns = {
    }

    def _prepare_invoice(self, cr, uid, partner, journal_id=None, context=None):
        """
        Se pueden agregar el name origin y reference, después de llamar a esta funcion, por ejemplo
            invoice_vals = self._prepare_invoice (cr, uid, partner, jorunal_id, context)
            invoice_vals['name'] = ''
            invoice_vals['origin'] = ''
            invoice_vals['reference'] = ''
        Prepare the dict of values to create the new invoice for a
           sales order. This method may be overridden to implement custom
           invoice generation (making sure to call super() to establish
           a clean extension chain).

           :param browse_record order: sale.order record to invoice
           :param list(int) line: list of invoice line IDs that must be
                                  attached to the invoice
           :return: dict of value to create() the invoice
        """
        if context is None:
            context = {}
        if journal_id is None:
            journal_ids = self.pool.get('account.journal').search(
                cr,
                uid,
                [('type', '=', 'sale'),
                ('company_id', '=', partner.company_id.id)],
                limit=1)
            if not journal_ids:
                raise except_orm(_('Error!'),
                    ('Please define sales journal for this company: "%s" (id:%d).') % (partner.company_id.name, partner.company_id.id))
            journal_id = journal_ids[0]
        invoice_vals = {
            'type': 'out_invoice',
            'account_id': partner.property_account_receivable.id,
            'partner_id': partner.id,
            'journal_id': journal_id,
            # 'invoice_line': [(6, 0, lines)],
            'currency_id': partner.property_product_pricelist.currency_id.id,
            'payment_term': partner.property_payment_term.id or False,
            'fiscal_position': partner.property_account_position.id,
            'date_invoice': context.get('date_invoice', False),
            'company_id': partner.company_id.id,
            'user_id': partner.user_id.id or False
        }
        return invoice_vals

    def process_interests(self, cr, uid, ids=None, context=None):
        if context is None:
            context = {}
        if ids is None:
            ids = self.search(cr, uid, [], context=context)
        company_obj = self.pool['res.company']
        company_ids = company_obj.search(cr, 1, [], context=context)
        context['date_invoice'] = time.strftime(DEFAULT_SERVER_DATE_FORMAT)
        for company in company_obj.browse(cr, 1, company_ids, context=context):
            if company.debt_interest_period:
                date_from = datetime.strftime(
                    date.today() + relativedelta(months=-company.debt_interest_period), DEFAULT_SERVER_DATE_FORMAT)
                date_to = time.strftime(DEFAULT_SERVER_DATE_FORMAT)
                self.calculate_interest(
                    cr, 1, ids, date_from, date_to, context=context)

    def _prepare_description(self, cr, uid, invoice, date_start, date_end, balance, interest_rate, context=None):
        date_diff = datetime.strptime(
            date_end, '%Y-%m-%d') - datetime.strptime(date_start, '%Y-%m-%d')

        tmp_date_from = datetime.strptime(date_start, '%Y-%m-%d')
        tmp_date_from = tmp_date_from.strftime('%d-%m-%y')
        tmp_date_to = datetime.strptime(date_end, '%Y-%m-%d')
        tmp_date_to = tmp_date_to.strftime('%d-%m-%y')

        move = invoice.move_id.name

        comment = _('Punitive Interests Invoice: ') + \
            move.replace(',', ' ') + '. '
        comment += _('Period: ') + tmp_date_from + '/' + tmp_date_to + ', '
        comment += str(date_diff.days) + _(' days. ')
        comment += _('Base(ARS): ') + str(balance) + ', '
        comment += _('Interest Rate(%): ') + str(interest_rate)

        return comment

    def calc_interests(self, cr, uid, dt_from, dt_to, balance, in_rate):
        date_diff = datetime.strptime(
            dt_to, '%Y-%m-%d') - datetime.strptime(dt_from, '%Y-%m-%d')
        interest_porcent = in_rate / 100
        interest_days = float(date_diff.days) / 365
        return interest_days * interest_porcent * balance

    def calculate_interest(self, cr, uid, ids, date_from, date_to, exclude_debit_note=True, company_id=False, context=None):

        if context is None:
            context = {}
        limit_value = 0
        invoice_obj = self.pool.get('account.invoice')
        invoice_line_obj = self.pool.get('account.invoice.line')
        account_move_line_obj = self.pool.get('account.move.line')
        account_account_obj = self.pool.get('account.account')
        user = self.pool.get('res.users').browse(cr, uid, uid, context)
        # If not company defined we use the user company
        if not company_id:
            company_id = user.company_id.id
        # for partner in self.browse(cr, uid, [73], context=context):
        for partner in self.browse(cr, uid, ids, context=context):
            journal_domain = [
                ('type', '=', 'sale'),
                ('company_id', '=', company_id),
                ]
                # Ahora el debit se elije en la invoice
                # ('afip_document_class_id.document_type', '=', 'debit_note')

            journal_ids = self.pool.get('account.journal').search(
                cr, uid, journal_domain, limit=1)
            if not journal_ids:
                raise except_orm(_('Error!'),
                                     _('Please define sales journal for this company id = %d.') % (company_id))

            # TODO si se quiere mejorar, habria que poder setear algun diarion en algun lugar que se quiera usar pore defecto, y tal vez un document type (si el diario usa doucments)
            journal_id = journal_ids[0]

            values = {}
            interest = 0

            move_line_domain = [
                ('partner_id', '=', partner.id),
                ('journal_id.type', 'in', ['sale']),
                ('account_id.type', '=', 'receivable'),
                ('company_id', '=', company_id),
                # No se puede buscar por amoun_residual porque es una funcion
                # ('amount_residual', '>', 0),
                # We add this line for filtering thos moves that reconciled
                ('reconcile_id', '=', False),
                ('account_id.account_account_interest_ids',
                 '!=', False),
                ('date_maturity', '<', date_to)
            ]
            if exclude_debit_note:
                move_line_domain.extend([
                    '|',
                    ('invoice.afip_document_class_id', '=', False),
                    ('invoice.afip_document_class_id.document_type',
                        '!=',
                        'debit_note')])
            move_line_ids = account_move_line_obj.search(
                cr, uid, move_line_domain, order='date_maturity')

            # We generate a list of partial reconcile ids
            partial_reconcile_ids = []
            for line in account_move_line_obj.browse(cr, uid, move_line_ids):
                if line.date_maturity < date_from:
                    date_start = date_from
                else:
                    date_start = line.date_maturity

                balance = line.amount_residual

                if balance <= 0:
                    continue

                interest_data = account_account_obj.get_active_interest_data(
                    cr, uid, [line.account_id.id], date_from, date_to, context=context)
                print 'interest_data', interest_data
                if line.account_id.id in interest_data:
                    interest_rate = interest_data[line.account_id.id].interest_rate
                    account_id = interest_data[
                        line.account_id.id].interest_account_id.id
                    analytic_id = interest_data[
                        line.account_id.id].analytic_account_id.id or False

                    if line.reconcile_partial_id:
                        # we check if we have already make the appointemnt for this
                        # account move
                        if line.id in partial_reconcile_ids:
                            for partial_reconcile_id in line.reconcile_partial_id.line_partial_ids:
                                partial_reconcile_ids.append(
                                    partial_reconcile_id.id)
                            continue

                        for partial_reconcile_id in line.reconcile_partial_id.line_partial_ids:
                            partial_reconcile_ids.append(partial_reconcile_id.id)
                        # partial_reconcile_ids += line.reconcile_partial_id.line_partial_ids
                        print partial_reconcile_ids
    # We replace the original way it calculate when partial reconliation
                    # if line.reconcile:
                    #     print 'aaaaaaaaaaaaaa'
                    #     print line.ref
                    #     move_line_all_ids =  account_move_line_obj.search(cr, uid, [
                    # Removed becasuse we have add the filter of reconciled = False
                    # '|',
                    # ('reconcile_id.name', '=', line.reconcile),
                    #                                                                 ('reconcile_partial_id.name', '=', line.reconcile),
                    #                                                                 ('id', '!=', line.id),
                    # ('date', '<', date_to),
                    #                                                                 ], order='date')
                    #     print move_line_all_ids

                    # for line_all in account_move_line_obj.browse(cr, uid,
                    # move_line_all_ids, context=context):

                    #         if line_all.date <= date_start:
                    #             balance -= line_all.credit
                    #         else:
                    #             interest_res = self.calc_interests(cr, uid, date_start, line_all.date, balance, interest_rate)

                    #             comment = self._prepare_description(cr, uid, line, date_start, line_all.date, balance, interest_rate)
                    #             values[len(values)] = [comment, round(interest_res,2), line.move_id.id]

                    #             interest += interest_res
                    #             balance -= line_all.credit
                    #             date_start = line_all.date

                    #     if round(balance,2) > 0:
                    #         interest_res = self.calc_interests(cr, uid, date_start, date_to, balance, interest_rate)
                    #         comment = self._prepare_description(cr, uid, line, date_start, date_to, balance, interest_rate)
                    #         values[len(values)] = [comment, round(interest_res,2), line.move_id.id]
                    #         interest += interest_res

                    # else:
                    #     interest_res = self.calc_interests(cr, uid, date_start, date_to, balance, interest_rate)
                    #     comment = self._prepare_description(cr, uid, line, date_start, date_to, balance, interest_rate)
                    #     values[len(values)] = [comment, round(interest_res,2), line.move_id.id]
                    #     interest += interest_res
                    interest_res = self.calc_interests(
                        cr, uid, date_start, date_to, balance, interest_rate)
                    comment = self._prepare_description(
                        cr, uid, line, date_start, date_to, balance, interest_rate)
                    values[len(values)] = [
                        comment, round(interest_res, 2), line.move_id.id]
                    interest += interest_res

            # if values:
            if values and round(interest, 2) > limit_value:
            # if True:
                invoice_vals = self._prepare_invoice(
                    cr, uid, partner, journal_id, context=context)
                tmp_date_from = datetime.strptime(date_from, '%Y-%m-%d')
                tmp_date_from = tmp_date_from.strftime('%d-%m-%y')

                tmp_date_to = datetime.strptime(date_to, '%Y-%m-%d')
                tmp_date_to = tmp_date_to.strftime('%d-%m-%y')

                invoice_vals['name'] = ''
                invoice_vals['comment'] = _(
                    'Punitive Interests ') + tmp_date_from + '/' + tmp_date_to
                invoice_vals['origin'] = invoice_vals['reference'] = _(
                    'Interests ') + tmp_date_from + '/' + tmp_date_to
                inv_id = invoice_obj.create(cr, uid, invoice_vals)

                for pos in values:
                    if values[pos][1] > 0:
                        invoice_line_obj.create(cr, uid, {
                            'name': values[pos][0],
                            'origin': '',
                            'invoice_id': inv_id,
                            'account_id': account_id,
                            'account_analytic_id': analytic_id,
                            'price_unit': values[pos][1],
                            'quantity': 1
                        })

        return True
