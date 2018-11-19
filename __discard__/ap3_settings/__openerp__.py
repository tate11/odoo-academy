# -*- coding: utf-8 -*-
{
    'name': "AP3 Settings",

    'summary': """
        Settings to be used in Academia Postal 3""",

    'description': """
        Settings to be used in Academia Postal 3
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
        'academy_base',
        'academy_tests'
    ],

    # always loaded
    'data': [
        'data/report_paperformat.xml',

        # 'views/external_layout.xml',
        'views/academy_test_report.xml',
        'views/academy_test_report_ayto.xml',
        'views/academy_post_tests_template.xml',
        'views/academy_post_test_template.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'js': [
    ],
    'css': [
    ],

    'license': 'AGPL-3'
}
