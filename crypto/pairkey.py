# -*- coding: utf-8 -*-
import os
from M2Crypto import BIO, Rand, SMIME, EVP, RSA, X509
from openerp import netsvc
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _

class pairkey(osv.osv):
    _name = "crypto.pairkey"
    _columns = {
        'name': fields.char('Name', size=256, select=True),
        'user_id': fields.many2one('res.users', 'Owner',
                                   select=True, 
                                   help='Owner of the key. The only who can view, import and export the key.'
                                  ),
        'group_id': fields.many2one('res.groups', 'User group',
                                    select=True,
                                    help='Users who use the pairkey.'),
        'pub': fields.text('Public key', 
                           readonly=True, states={'draft': [('readonly',False)]}, 
                           help='Public key in PEM format.'),
        'key': fields.text('Private key', readonly=True, states={'draft': [('readonly',False)]},
                          help='Private key in PEM format.'),
        'state': fields.selection([
                ('draft', 'Draft'),
                ('confirmed', 'Confirmed'),
                ('cancel', 'Cancelled'),
            ], 'State', select=True, readonly=True,
            help='* The \'Draft\' state is used when a user is creating a new pair key. Warning: everybody can see the key.\
            \n* The \'Confirmed\' state is used when the key is completed with public or private key.\
            \n* The \'Canceled\' state is used when the key is not more used. You cant use this key again.'),
    }
    _defaults = {
        'state': 'draft',
    }

    def action_validate(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        pairkeys = self.read(cr, uid, ids, ['key', 'pub'], context=context)
        confirm_ids = []
        for pk in pairkeys:
            # Check public key
            try:
                PUB = BIO.MemoryBuffer(pk['pub'].encode('ascii'))
                RSA.load_pub_key_bio(PUB)
                pub = True
            except:
                pub = False
            # Check private key
            try:
                RSA.load_key_string(pk['key'].encode('ascii'))
                key = True
            except:
                key = False
            if key or pub:
                confirm_ids.append(pk['id'])
            else:
                raise osv.except_osv(_('Invalid action !'),
                                     _('Cannot confirm invalid pairkeys. You need provide private and public keys in PEM format.'))
        return True

    def action_generate(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.generate_keys(cr, uid, ids, context=context)
        return self.action_validate(cr, uid, ids, context=context)

    def as_pem(self, cr, uid, ids):
        """
        Return pairkey in pem format. 
        """
        r = {}
        for pairkey in self.browse(cr, uid, ids):
            if pairkey.key: 
                r[pairkey.id] = pairkey.key.encode('ascii')
            else:
                r[pairkey.id] = ''
            if pairkey.pub:
                r[pairkey.id] += pairkey.pub.encode('ascii')
        return r

    def as_rsa(self, cr, uid, ids):
        """
        Return RSA object. 
        """
        return dict((k,RSA.load_key_string(v)) for k,v in self.as_pem(cr, uid, ids).items())

    def as_pkey(self, cr, uid, ids):
        """
        Return PKey object.
        """
        def set_key(rsa):
            pk = EVP.PKey()
            pk.assign_rsa(rsa)
            return pk
        return dict((k,set_key(v)) for k,v in self.as_rsa(cr, uid, ids).items())

    def generate_keys(self, cr, uid, ids, key_length=1024, key_gen_number=0x10001, context=None):
        """
        Generate key pairs: private and public.
        """
        if context is None:
            context = {}
        for signer in self.browse(cr, uid, ids):
            # Random seed
            Rand.rand_seed (os.urandom(key_length))
            # Generate key pair
            key = RSA.gen_key (key_length, key_gen_number, lambda *x: None)
            # Create memory buffers
            pri_mem = BIO.MemoryBuffer()
            pub_mem = BIO.MemoryBuffer()
            # Save keys to buffers
            key.save_key_bio(pri_mem, None)
            key.save_pub_key_bio(pub_mem)

            w = {
                'key': pri_mem.getvalue(),
                'pub': pub_mem.getvalue(),
            }
            self.write(cr, uid, signer.id, w)
        return True

    def generate_certificate_request(self, cr, uid, ids,
                                     x509_name,
                                     context=None):
        """
        Generate new certificate request for pairkey.
        """
        if context is None:
            context = {}
        r = {}
        for signer in self.browse(cr, uid, ids):
            # Create certificate structure
            pk = EVP.PKey()
            req = X509.Request()
            pem_string = signer.key.encode('ascii') + '\n' + signer.pub.encode('ascii')
            rsa = RSA.load_key_string(pem_string)
            pk.assign_rsa(rsa)
            req.set_pubkey(pk)
            req.set_subject(x509_name)

            # Crete certificate object
            certificate_obj = self.pool.get('crypto.certificate')
            w = {
                'name': x509_name.as_text(),
                'csr': req.as_pem(),
                'pairkey_id': signer.id,
            }
            r[signer.id] = certificate_obj.create(cr, uid, w)
        return r

    def action_wfk_set_draft(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state':'draft'})
        wf_service = netsvc.LocalService("workflow")
        for obj_id in ids:
            wf_service.trg_delete(uid, 'crypto.pairkey', obj_id, cr)
            wf_service.trg_create(uid, 'crypto.pairkey', obj_id, cr)
        return True  

pairkey()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
