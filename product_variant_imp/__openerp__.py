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
    'name': 'Product Variant Improvements',
    'category': 'base.module_category_knowledge_management',
    'description': """
Product Variant Improvements
============================
TODO para agregar bien y traducir:
Ya estaría esto, por favor probarlo (mejor en bd de test primero, aunque no pasaría nada de necesitar desisntalarlo). 
El modulo se llama "product_variant_imp" y tmb es instlable desde adhoc config (subcategoría productos). 

Para cada atributo se debe marcar si se quiere incluirlo o no en el nombre (por defecto no van incluido). 

Cada vez que marques un atributo y guardes, es probable que tarde un poquito porque a todos los productos que usen ese atributo le va a crear un mobre con eso. 

""",
    'author': 'ADHOC SA.',
    'website': 'www.adhoc.com.ar',
    'license': 'AGPL-3',
    'depends': ['product'],
    'demo': [
        'product_demo.xml',
    ],
    'data': [
        'product_view.xml',
    ],
    'installable': True
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
