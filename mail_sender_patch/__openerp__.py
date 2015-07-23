# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015  ADHOC SA  (http://www.adhoc.com.ar)
#    All Rights Reserved.
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
{
    "name": "Mail Sender Patch",
    "version": "1.0",
    'author':  'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    "category": "Accounting",
    "description": """ 
Mail Sender Patch
=================
21/05/2015:
    Depreciado porque al parece no ser más necesario...
    En realidad en algunas bds sigue siendo necesario, lo reactivamos

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
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
