# -*- coding: utf-8 -*-
{
    'name': 'Academy Tests',

    'summary': '''
        Store and manage information about tests and their questions''',

    'description': '''
        Store and manage information about tests and their questions
    ''',

    'author': 'Jorge Soto Garcia',
    'website': 'https://github.com/sotogarcia',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Academy',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'mail',
        # 'report',
        # 'website',
        'academy_base',
    ],

    # always loaded
    'data': [
        'data/academy_test_level_data.xml',

        'security/academy_test_answer.xml',
        'security/academy_test_answers_table.xml',
        'security/academy_test_category.xml',
        'security/academy_test_level.xml',
        'security/academy_test_question.xml',
        'security/academy_test_question_impugnment.xml',
        'security/academy_test_tag.xml',
        'security/academy_test.xml',
        'security/academy_test_academy_test_question_rel.xml',
        'security/academy_test_topic.xml',

        'views/academy_tests.xml',
        'views/academy_test_answer_view.xml',
        'views/academy_test_category_view.xml',
        'views/academy_test_level_view.xml',
        'views/academy_test_question_impugnment_view.xml',
        'views/academy_test_question_view.xml',
        'views/academy_test_tag_view.xml',
        'views/academy_test_academy_test_question_rel.xml',
        'views/academy_test_view.xml',
        'views/academy_test_topic_view.xml',
        'views/ir_attachment_view.xml',

        'views/academy_test_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/academy_test_tag_demo.xml',
        'demo/academy_test_topic_demo.xml',
        'demo/academy_test_category_demo.xml',
        'demo/academy_test_test_demo.xml',
        'demo/academy_test_question_demo.xml',
        'demo/academy_test_answer_demo.xml',
        'demo/academy_test_test_question_rel_demo.xml',
    ],
    'js': [
        'static/src/js/academy_tests.js'
    ],
    'css': [
        'static/src/css/styles-backend.css',
        'static/src/css/academy_test_report.css'
    ],

    'license': 'AGPL-3'
}

