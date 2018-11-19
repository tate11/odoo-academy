# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Management Solution
#
#    Copyright (c) All rights reserved:
#        (c) 2015
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses
#
###############################################################################
{
    'name': 'Academy Exercise Tools',
    'summary': 'Academy Exercise Tools Module',
    'version': '1.0',

    'description': """
Academy Exercise Tools Module.
==============================================


    """,

    'author': 'Jorge Soto García',
    'maintainer': 'Jorge Soto García',
    'contributors': [' <sotogarcia@gmail.com>'],

    'website': 'http://www.gitlab.com/',

    'license': 'AGPL-3',
    'category': 'Academy',

    'depends': [
        'academy_base'
    ],
    'external_dependencies': {
        'python': [
        ],
    },
    'data': [
        'views/academy_rebasing_tools.xml',
        'views/academy_rebasing_exercise_view.xml',
        'views/academy_rebasing_exercise_item_view.xml',
        'views/academy_rebasing_exercise_report.xml'
    ],
    'demo': [
    ],
    'js': [
    ],
    'css': [
    ],
    'qweb': [
    ],
    'images': [
    ],
    'test': [
    ],

    'installable': True
}
