# -*- coding: utf-8 -*-
{'active': False,
    'author': 'Ingenieria ADHOC.',
    'category': 'base.module_category_knowledge_management',
    'demo_xml': [],
    'depends': ['product'],
    'description': """
Product Variant Improvements
============================
TODO para agregar bien y traducir:
Ya estaría esto, por favor probarlo (mejor en bd de test primero, aunque no pasaría nada de necesitar desisntalarlo). 
El modulo se llama "product_variant_imp" y tmb es instlable desde adhoc config (subcategoría productos). 

Para cada atributo se debe marcar si se quiere incluirlo o no en el nombre (por defecto no van incluido). 

Cada vez que marques un atributo y guardes, es probable que tarde un poquito porque a todos los productos que usen ese atributo le va a crear un mobre con eso. 

""",
    'init_xml': [],
    'installable': True,
    'license': 'AGPL-3',
    'name': 'Product Variant Improvements',
    'test': [],
    'data': [
        'product_view.xml',
    ],
    'website': 'www.ingadhoc.com'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
