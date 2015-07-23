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
{   'active': False,
    'author': u'ADHOC SA',
    'category': u'base.module_category_knowledge_management',
    'demo_xml': [],
    'depends': ['survey',],
    'description': u"""
Extends the functionality of the survey module in order to make assessments that are corrected automatically
""",
    'installable': True,
    'license': 'AGPL-3',
    'name': u'Academic Evaluations',
    'test': [
            ],
    'data': [
            'view/survey_view.xml',
            'security/ir.model.access.csv',
            'security/survey_security.xml',
            ],
    'version': u'1.0',
    'website': 'www.adhoc.com.ar'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
