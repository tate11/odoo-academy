# -*- coding: utf-8 -*-
{
    'name': "Academy Public Tendering",

    'summary': """
        Store and manage information about civil service entrance examination""",

    'description': """
        Store and manage information about civil service entrance examination
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
        'academy_base'
    ],

    # always loaded
    'data': [
        'data/res_partner_category_data.xml',
        'data/res_partner_data.xml',
        'data/academy_public_tendering_employment_group_data.xml',
        'data/academy_public_tendering_exam_type_data.xml',
        'data/academy_public_tendering_hiring_type_data.xml',
        'data/academy_public_tendering_vacancy_position_type.xml',
        'data/ir_cron.xml',

        'security/academy_public_tendering_hiring_type.xml',
        'security/academy_public_tendering_employment_group.xml',
        'security/academy_public_tendering_exam_type.xml',
        'security/academy_public_tendering_process.xml',
        'security/academy_public_tendering_vacancy_position_type.xml',
        'security/academy_public_tendering_vacancy_position.xml',

        'views/academy_public_tendering.xml',

        'views/academy_public_tendering_employment_group_view.xml',
        'views/academy_public_tendering_exam_type_view.xml',
        'views/academy_public_tendering_hiring_type_view.xml',
        'views/academy_public_tendering_vacancy_position_type_view.xml',
        'views/academy_public_tendering_vacancy_position_view.xml',
        'views/academy_public_tendering_process_view.xml',

        'views/academy_training_action_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/res_partner_demo.xml',
        'demo/academy_public_tendering_process_demo.xml',
        'demo/academy_public_tendering_vacancy_position_demo.xml',
    ],
    'js': [
    ],
    'css': [
    ],
}

