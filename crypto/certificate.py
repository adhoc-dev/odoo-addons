# -*- coding: utf-8 -*-
import os, time
from M2Crypto import BIO, Rand, SMIME, EVP, RSA, X509, ASN1
from openerp import netsvc
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
import logging

_logger = logging.getLogger(__name__)

class certificate(osv.osv):
    def _get_status(self, cr, uid, ids, field_name, arg, context=None):
        r = {}
        for cer in self.browse(cr, uid, ids):
            if not cer.csr and not cer.crt:
                r[cer.id] = 'empty'
            elif cer.csr and not cer.crt:
                try:
                    req = cer.get_request()[cer.id]
                    pkey = req.get_pubkey()
                    if req.verify(pkey):
                        r[cer.id] = 'valid_request'
                    else:
                        r[cer.id] = 'invalid_request'
                except:
                    r[cer.id] = 'invalid_request'
            elif cer.csr and cer.crt:
                try:
                    req = cer.get_request()[cer.id]
                    pkey = req.get_pubkey()
                    crt = cer.get_certificate()[cer.id]
                    r[cer.id] = 'valid' if crt.verify() and crt.verify(pkey) else 'invalid'
                except:
                    r[cer.id] = 'invalid'
            elif not cer.csr and cer.pairkey_id and cer.crt:
                pkey = cer.pairkey_id.as_pkey()[cer.pairkey_id.id]
                try:
                    crt = cer.get_certificate()[cer.id]
                    r[cer.id] = 'valid' if crt.verify() and crt.verify(pkey) else 'invalid'
                except:
                    r[cer.id] = 'invalid'

            else:
                r[cer.id] = 'Invalid'
        return r

    _name = "crypto.certificate"
    _columns = {
        'name': fields.char('Name',
                            size=256,
                            states={'draft': [('readonly',False)]}, 
                            required=True),
        'pairkey_id': fields.many2one('crypto.pairkey', 'Key pair',
                                      readonly=True,
                                      required=True,
                                      states={'draft': [('readonly',False)]}),
        'csr': fields.text('Request Certificate',
                           readonly=True,
                           states={'draft': [('readonly',False)]}, 
                           help='Certificate Request in PEM format.'),
        'crt': fields.text('Certificate',
                           readonly=True,
                           states={'draft': [('readonly',False)], 'waiting':[('readonly',False)]}, 
                           help='Certificate in PEM format.'),
        'status': fields.function(_get_status, method=True, string='Status', type='char',
                                 help='Certificate Status'),
        'state': fields.selection([
                ('draft', 'Draft'),
                ('waiting', 'Waiting'),
                ('confirmed', 'Confirmed'),
                ('cancel', 'Cancelled'),
            ], 'State', select=True, readonly=True,
            help='* The \'Draft\' state is used when a user is creating a new pair key. Warning: everybody can see the key.\
            \n* The \'Waiting\' state is used when a request has send to Certificate Authority and is waiting for response.\
            \n* The \'Confirmed\' state is used when a certificate is valid.\
            \n* The \'Canceled\' state is used when the key is not more used. You cant use this key again.'),
    }
    _defaults = {
        'state': 'draft',
    }

    def _action_validate(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        certs = self.read(cr, uid, ids, ['name', 'status', 'state'], context=context)
        confirm_ids = []
        waiting_ids = []
        for cert in certs:
            status = cert['status']
            state = cert['state']
            if status in 'valid_request' and state == 'draft':
                waiting_ids.append(cert['id'])
            elif status == 'valid' and state in [ 'draft', 'waiting' ]:
                confirm_ids.append(cert['id'])
            else:
                raise osv.except_osv(_('Invalid action !'),
                                     _('Perhaps you want to insert an invalid request or certificate, or you want approve an invalid certificate with an valid request. Status: %s, State: %s'))
        self.write(cr, uid, confirm_ids, {'state': 'confirmed'}, context=context)
        self.write(cr, uid, waiting_ids, {'state': 'waiting'}, context=context)
        return True

    def action_cancel(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'cancel'}, context=context)
        return True

    def get_request(self, cr, uid, ids, context=None):
        """
        Return Request object.
        """
        r = {}
        for cert in self.browse(cr, uid, ids):
            if cert.csr:
                try:
                   r[cert.id] = X509.load_request_string(cert.csr.encode('ascii'))
                except X509.X509Error as detail:
                   _logger.warn(detail)
                   r[cert.id] = None
            else:
                r[cert.id] = None
        return r

    def get_certificate(self, cr, uid, ids, context=None):
        """
        Return Certificate object.
        """
        r = {}
        for cert in self.browse(cr, uid, ids):
            if cert.crt:
                r[cert.id] = X509.load_cert_string(cert.crt.encode('ascii'))
            else:
                r[cert.id] = None
        return r

    def generate_certificate(self, cr, uid, ids, issuer,
                             ext=None, serial_number=1, version=2,
                             date_begin=None,
                             date_end=None,
                             expiration=365,
                             context=None):
        """
        Generate certificate
        """
        for item in self.browse(cr, uid, ids):
            if item.status == 'valid_request':
                # Get request data
                pk = item.pairkey_id.as_pkey()[item.pairkey_id.id]
                req = item.get_request()[item.id]
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
                w = { 'crt': cert.as_pem() }
                self.write(cr, uid, item.id, w)


    def smime(self, cr, uid, ids, message, context=None):
        """
        Sign message in SMIME format.
        """
        r = {}
        for cert in self.browse(cr, uid, ids):
            #if cert.status == 'valid': # EXTRANGE: Invalid certificates can be used for sign!
            if True:
                smime = SMIME.SMIME()
                ks = BIO.MemoryBuffer(cert.pairkey_id.key.encode('ascii'))
                cs = BIO.MemoryBuffer(cert.crt.encode('ascii'))
                bf = BIO.MemoryBuffer(str(message))
                out = BIO.MemoryBuffer()
                try:
                    smime.load_key_bio(ks, cs)
                except EVP.EVPError:
                    raise osv.except_osv(_('Error in Key and Certificate strings !'), _('Please check if private key and certificate are in ASCII PEM format.'))
                sbf = smime.sign(bf)
                smime.write(out, sbf)
                r[cert.id] = out.read()
            else:
                raise osv.except_osv(_('This certificate is not ready to sign any message !'), _('Please set a certificate to continue. You must send your certification request to a authoritative certificator to get one, or execute a self sign certification'))
        return r

    def have_csr(self, cr, uid, ids, can_raise=True, context=None):
        """
        Verify if certificate request is valid
        """
        r = {}
        for cer in self.browse(cr, uid, ids):
            csr = cer.csr
            if not csr and can_raise:
                raise osv.except_osv(_('Invalid action !'),
                                     _('Please, set the certification request string to continue or generate one.'))

            req = cer.get_request()[cer.id]
            if req is None and can_raise:
                raise osv.except_osv(_('Invalid action !'),
                                     _('Your certificate request string is invalid. Check if you forgot the header CERTIFICATE REQUEST or forgot/append end of lines.'))

            pkey = req.get_pubkey()
            if not req.verify(pkey) and can_raise:
                raise osv.except_osv(_('Invalid action !'),
                                     _('Your certificate request is not compatible with the private key.'))
            r[cer.id] = True
        return r

    def have_crt(self, cr, uid, ids, can_raise=True, context=None):
        """
        Verify if certificate is well formed
        """
        r = {}
        for cer in self.browse(cr, uid, ids):
            crt = cer.crt
            if not crt and can_raise:
                raise osv.except_osv(_('Invalid action !'),
                                     _('Please, set the certification string to continue.'))

            certificate = cer.get_certificate()[cer.id]
            if certificate is None and can_raise:
                raise osv.except_osv(_('Invalid action !'),
                             _('Your certificate string is invalid. Check if you forgot the header CERTIFICATE or forgot/append end of lines.'))

            r[cer.id] = True
        return r

    def action_wfk_set_draft(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state':'draft'})
        wf_service = netsvc.LocalService("workflow")
        for obj_id in ids:
            wf_service.trg_delete(uid, 'crypto.certificate', obj_id, cr)
            wf_service.trg_create(uid, 'crypto.certificate', obj_id, cr)
        return True  

certificate()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
