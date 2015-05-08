# -*- coding: utf-8 -*-
import os, time
from M2Crypto import BIO, Rand, SMIME, EVP, RSA, X509, ASN1
from openerp.exceptions import Warning
from openerp import fields, models, api
from openerp.tools.translate import _
import logging

_logger = logging.getLogger(__name__)


class certificate(models.Model):

    @api.one
    @api.depends()
    def _get_status(self):
        if not self.csr and not self.crt:
            status = 'empty'
        elif self.csr and not self.crt:
            try:
                req = self.get_request()[self.id]
                pkey = req.get_pubkey()
                if req.verify(pkey):
                    status = 'valid_request'
                else:
                    status = 'invalid_request'
            except:
                status = 'invalid_request'
        elif self.csr and self.crt:
            try:
                req = self.get_request()[self.id]
                pkey = req.get_pubkey()
                crt = self.get_certificate()[self.id]
                status = 'valid' if crt.verify() and crt.verify(pkey) else 'invalid'
            except:
                status = 'invalid'
        elif not self.csr and self.pairkey_id and self.crt:
            pkey = self.pairkey_id.as_pkey()[self.pairkey_id.id]
            try:
                crt = self.get_certificate()[self.id]
                status = 'valid' if crt.verify() and crt.verify(pkey) else 'invalid'
            except:
                status = 'invalid'

        else:
            status = 'Invalid'
        self.status = status

    _name = "crypto.certificate"

    name = fields.Char(
        'Name',
        size=256,
        states={'draft': [('readonly',False)]},
        required=True
        )
    pairkey_id = fields.Many2one(
        'crypto.pairkey',
        'Key pair',
        readonly=True,
        required=True,
        states={'draft': [('readonly', False)]}
        )
    csr = fields.Text(
        'Request Certificate',
        readonly=True,
        states={'draft': [('readonly', False)]},
        help='Certificate Request in PEM format.'
        )
    crt = fields.Text(
        'Certificate',
        readonly=True,
        states={
            'draft': [('readonly', False)], 'waiting': [('readonly', False)]},
        help='Certificate in PEM format.'
        )
    status = fields.Char(
        compute='_get_status',
        string='Status',
        help='Certificate Status'
        )
    state = fields.Selection([
            ('draft', 'Draft'),
            ('waiting', 'Waiting'),
            ('confirmed', 'Confirmed'),
            ('cancel', 'Cancelled'),
        ],
        'State',
        select=True,
        readonly=True,
        default='draft',
        help='* The \'Draft\' state is used when a user is creating a new pair key. Warning: everybody can see the key.\
        \n* The \'Waiting\' state is used when a request has send to Certificate Authority and is waiting for response.\
        \n* The \'Confirmed\' state is used when a certificate is valid.\
        \n* The \'Canceled\' state is used when the key is not more used. You cant use this key again.')

    @api.multi
    def _action_validate(self):
        confirm_ids = []
        waiting_ids = []
        for cert in self:
            status = self.status
            state = self.state
            if status in 'valid_request' and state == 'draft':
                waiting_ids.append(cert['id'])
            elif status == 'valid' and state in ['draft', 'waiting']:
                confirm_ids.append(cert['id'])
            else:
                raise Warning(_('Invalid action! Perhaps you want to insert an invalid request or certificate, or you want approve an invalid certificate with an valid request. Status: %s, State: %s'))
        self.browse(confirm_ids).write({'state': 'confirmed'})
        self.browse(waiting_ids).write({'state': 'waiting'})
        return True

    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancel'})
        return True

    @api.one
    def get_request(self):
        """
        Return Request object.
        """
        if self.csr:
            try:
                request = X509.load_request_string(self.csr.encode('ascii'))
            except X509.X509Error as detail:
                _logger.warn(detail)
                request = None
        else:
            request = None
        return request

    @api.one
    def get_certificate(self, cr, uid, ids, context=None):
        """
        Return Certificate object.
        """
        if self.crt:
            certificate = X509.load_cert_string(self.crt.encode('ascii'))
        else:
            certificate = None
        return certificate

    @api.one
    def generate_certificate(
            self, issuer, ext=None, serial_number=1, version=2,
            date_begin=None, date_end=None, expiration=365):
        """
        Generate certificate
        """
        if self.status == 'valid_request':
            # Get request data
            pk = self.pairkey_id.as_pkey()[self.pairkey_id.id]
            req = self.get_request()[self.id]
            sub = req.get_subject()
            pkey = req.get_pubkey()
            # Building certificate
            cert = X509.X509()
            cert.set_serial_number(serial_number)
            cert.set_version(version)
            cert.set_subject(sub)

            now = ASN1.ASN1_UTCTIME()
            if date_begin is None:
                t = long(time.time()) + time.timezone
                now.set_time(t)
            else:
                now.set_datetime(date_begin)

            nowPlusYear = ASN1.ASN1_UTCTIME()
            if date_end is None:
                nowPlusYear.set_time(t + 60 * 60 * 24 * expiration)
            else:
                nowPlusYear.set_datetime(date_end)

            cert.set_not_before(now)
            cert.set_not_after(nowPlusYear)
            cert.set_issuer(issuer)
            cert.set_pubkey(pkey)
            cert.set_pubkey(cert.get_pubkey())
            if ext:
                cert.add_ext(ext)
            cert.sign(pk, 'sha1')
            w = {'crt': cert.as_pem()}
            self.write(self.id, w)

    @api.one
    def smime(self, message):
        """
        Sign message in SMIME format.
        """
        #if cert.status == 'valid': # EXTRANGE: Invalid certificates can be used for sign!
        res = False
        if True:
            smime = SMIME.SMIME()
            ks = BIO.MemoryBuffer(self.pairkey_id.key.encode('ascii'))
            cs = BIO.MemoryBuffer(self.crt.encode('ascii'))
            bf = BIO.MemoryBuffer(str(message))
            out = BIO.MemoryBuffer()
            try:
                smime.load_key_bio(ks, cs)
            except EVP.EVPError:
                raise Warning(_(
                    'Error in Key and Certificate strings! Please check if private key and certificate are in ASCII PEM format.'))
            sbf = smime.sign(bf)
            smime.write(out, sbf)
            res = out.read()
        else:
            raise Warning(_(
                'This certificate is not ready to sign any message! Please set a certificate to continue. You must send your certification request to a authoritative certificator to get one, or execute a self sign certification'))
        return res

    @api.one
    def have_csr(self, can_raise=True):
        """
        Verify if certificate request is valid
        """
        csr = self.csr
        if not csr and can_raise:
            raise Warning(_(
                'Invalid action! Please, set the certification request string to continue or generate one.'))

        req = self.get_request()[self.id]
        if req is None and can_raise:
            raise Warning(_(
                'Invalid action! Your certificate request string is invalid. Check if you forgot the header CERTIFICATE REQUEST or forgot/append end of lines.'))

        pkey = req.get_pubkey()
        if not req.verify(pkey) and can_raise:
            raise Warning(_(
                'Invalid action! Your certificate request is not compatible with the private key.'))
        return True

    @api.one
    def have_crt(self, can_raise=True):
        """
        Verify if certificate is well formed
        """
        crt = self.crt
        if not crt and can_raise:
            raise Warning(_(
                'Invalid action! Please, set the certification string to continue.'))

        certificate = self.get_certificate()[self.id]
        if certificate is None and can_raise:
            raise Warning(_(
                'Invalid action! Your certificate string is invalid. Check if you forgot the header CERTIFICATE or forgot/append end of lines.'))

        return True

    @api.multi
    def action_wfk_set_draft(self):
        self.write({'state': 'draft'})
        self.delete_workflow()
        self.create_workflow()
        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
