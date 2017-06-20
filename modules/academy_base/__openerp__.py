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
        'data/ir_actions_server_data.xml',

        'views/academy_base.xml',

        'views/appointment_manager_view.xml',

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

        'views/academy_training_session_view.xml',
        'views/academy_training_resource_view.xml',
        'views/academy_training_action_sign_up_view.xml',
        'views/academy_training_session_itemisation_view.xml',
        'views/academy_training_session_attendance_view.xml',

        'security/academy_application_scope.xml',
        'security/academy_base.xml',
        'security/academy_competency_unit.xml',
        'security/academy_knowledge_area.xml',
        'security/academy_professional_area.xml',
        'security/academy_professional_category.xml',
        'security/academy_professional_family.xml',
        'security/academy_professional_qualification.xml',
        'security/academy_qualification_level.xml',
        'security/academy_training_action.xml',
        'security/academy_training_action_sign_up.xml',
        'security/academy_training_activity.xml',
        'security/academy_training_methodology.xml',
        'security/academy_training_modality.xml',
        'security/academy_training_module.xml',
        'security/academy_training_resource.xml',
        'security/academy_training_session.xml',
        'security/academy_training_session_attendance.xml',
        'security/academy_training_session_itemisation.xml',
        'security/academy_training_unit.xml',
        'security/appointment_manager.xml',

        'wizard/academy_training_session_wizard.xml',

    ],
    'qweb': [
        'wizard/widget_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'js': [
        'static/src/js/appointment_manager.js'
    ],
    'css': [
        'static/src/css/academy_training_action_view.css',
        'static/src/css/academy_training_session_wizard.css'
    ],
    "external_dependencies": {
        "python" : []
    },
    'license': 'AGPL-3'
}
