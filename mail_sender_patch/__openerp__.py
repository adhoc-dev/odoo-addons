# -*- coding: utf-8 -*-
{
    "name": "Mail Sender Patch",
    "version": "1.0",
    'author':  'Ingeniería ADHOC',
    'website': 'www.ingadhoc.com.ar',
    "category": "Accounting",
    "description": """ 
Mail Sender Patch
=================
Este patch reemplaza el sender que utiliza odoo porque nuestro servidor smtp no permite que se loguee cualquiera.
Si agregamos el parametro "mail.bounce.alias" luego, a los emails de un modelo y recurso, les agrega la data y tmb son rechazados. Ver:
    * en mail/mail_mail.py
        if bounce_alias and catchall_domain:
                    if mail.model and mail.res_id:
Si no agregamos el paremtro "mail.bounce.alias" luego usa odoo-postmaster@alias pero nosotros no creamos una cuenta de envio para cada subdominio por lo cual tmb es rechazado. 

La alternativa seria instalar postfix y hacer los registros pertinences. 
Dejamos algunos posts relacionados a postfix y los commits en cuestion:

* ISSUE https://github.com/odoo/odoo/issues/3347
* un commit https://github.com/odoo-dev/odoo/commit/a4597fe34fcfa8dae28b156410080346bb33af33
* Sugerencias de odoo help https://www.odoo.com/es_ES/forum/help-1/question/how-to-set-up-e-mail-messaging-with-odoo-61796
* Configurar postfix con no se que https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-dkim-with-postfix-on-debian-wheezy
* otro postf para configurar postfix http://mhawthorne.net/posts/postfix-configuring-gmail-as-relay.html
    """,
    'depends': [
        'base',
    ],
    'data': [
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
