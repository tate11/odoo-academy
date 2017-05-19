# -*- coding: utf-8 -*-
{
    'name': "Academy Base",

    'summary': """
        Common information and behavior used by the academy modules""",

    'description': """
        Common information and behavior used by the academy modules
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
        'base'
    ],

    # always loaded
    'data': [
        'data/res_groups.xml',

        'views/academy_base.xml',
        'views/academy_training_methodology_view.xml',
        'views/academy_training_modality_view.xml',
        'views/academy_application_scope_view.xml',
        'views/academy_knowledge_area_view.xml',
        'views/academy_qualification_level_view.xml',
        'views/academy_professional_area_view.xml',
        'views/academy_professional_category_view.xml',
        'views/academy_professional_family_view.xml',
        'views/academy_professional_qualification_view.xml',

        'views/academy_training_unit_view.xml',
        'views/academy_training_module_view.xml',
        'views/academy_competency_unit_view.xml',
        'views/academy_training_action_view.xml',

        'views/res_parter_view.xml',
        'views/academy_training_action_sign_up_view.xml',
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
