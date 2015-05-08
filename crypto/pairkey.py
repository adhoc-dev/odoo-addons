# -*- coding: utf-8 -*-
import os
from M2Crypto import BIO, Rand, SMIME, EVP, RSA, X509
from openerp import fields, models, api, _
from openerp.exceptions import Warning


class pairkey(models.Model):
    _name = "crypto.pairkey"

    name = fields.Char(
        'Name', size=256, select=True)
    user_id = fields.Many2one(
        'res.users', 'Owner', select=True,
        help='Owner of the key. The only who can view, import and export the key.'
        )
    group_id = fields.Many2one(
        'res.groups', 'User group', select=True,
        help='Users who use the pairkey.'
        )
    pub = fields.Text(
        'Public key', readonly=True, states={'draft': [('readonly', False)]},
        help='Public key in PEM format.'
        )
    key = fields.Text(
        'Private key', readonly=True, states={'draft': [('readonly', False)]},
        help='Private key in PEM format.'
        )
    state = fields.Selection([
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('cancel', 'Cancelled'),
        ], 'State', select=True, readonly=True, default='draft',
        help='* The \'Draft\' state is used when a user is creating a new pair key. Warning: everybody can see the key.\
        \n* The \'Confirmed\' state is used when the key is completed with public or private key.\
        \n* The \'Canceled\' state is used when the key is not more used. You cant use this key again.')

    @api.multi
    def action_validate(self):
        confirm_ids = []
        for pk in self:
            # Check public key
            try:
                PUB = BIO.MemoryBuffer(pk.pub.encode('ascii'))
                RSA.load_pub_key_bio(PUB)
                pub = True
            except:
                pub = False
            # Check private key
            try:
                RSA.load_key_string(pk.key.encode('ascii'))
                key = True
            except:
                key = False
            if key or pub:
                confirm_ids.append(pk.id)
            else:
                raise Warning(_(
                    'Invalid action! Cannot confirm invalid pairkeys. You need provide private and public keys in PEM format.'))
        return True

    @api.multi
    def action_generate(self):
        self.generate_keys()
        return self.action_validate()

    @api.one
    def as_pem(self):
        """
        Return pairkey in pem format.
        """
        if self.key:
            res = self.key.encode('ascii')
        else:
            res = ''
        if self.pub:
            res += self.pub.encode('ascii')
        return res

    @api.multi
    def as_rsa(self):
        """
        Return RSA object.
        """
        return dict(
            (k, RSA.load_key_string(v)) for k, v in self.as_pem().items())

    @api.multi
    def as_pkey(self):
        """
        Return PKey object.
        """
        def set_key(rsa):
            pk = EVP.PKey()
            pk.assign_rsa(rsa)
            return pk
        return dict(
            (k, set_key(v)) for k, v in self.as_rsa().items())

    @api.multi
    def generate_keys(self, key_length=1024, key_gen_number=0x10001):
        """
        Generate key pairs: private and public.
        """
        for signer in self:
            # Random seed
            Rand.rand_seed(os.urandom(key_length))
            # Generate key pair
            key = RSA.gen_key(key_length, key_gen_number, lambda *x: None)
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
            signer.write(w)
        return True

    @api.one
    def generate_certificate_request(self, x509_name):
        """
        Generate new certificate request for pairkey.
        """
        # Create certificate structure
        pk = EVP.PKey()
        req = X509.Request()
        pem_string = self.key.encode('ascii') + '\n' + self.pub.encode('ascii')
        rsa = RSA.load_key_string(pem_string)
        pk.assign_rsa(rsa)
        req.set_pubkey(pk)
        req.set_subject(x509_name)
        w = {
            'name': x509_name.as_text(),
            'csr': req.as_pem(),
            'pairkey_id': self.id,
        }
        return self.env['crypto.certificate'].create(w)

    @api.multi
    def action_wfk_set_draft(self):
        self.write({'state': 'draft'})
        self.delete_workflow()
        self.create_workflow()
        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
