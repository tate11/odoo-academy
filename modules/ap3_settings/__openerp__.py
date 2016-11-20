# -*- coding: utf-8 -*-
{
    'name': "AP3 Settings",

    'summary': """
        Settings will be used in Academia Postal 3""",

    'description': """
        Settings will be used in Academia Postal 3
    """,

    'author': "Jorge Soto Garcia",
    'website': "https://github.com/sotogarcia",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Academy',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [

    ],

    # always loaded
    'data': [
        'data/report_paperformat.xml',
        'views/external_layout.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'js': [
    ],
    'css': [
    ],
}
