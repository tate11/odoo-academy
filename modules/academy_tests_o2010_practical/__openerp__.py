# -*- coding: utf-8 -*-
{
    'name': "Academy Tests - Microsoft Office 2010: Practical tests",

    'summary': """
        Tests questions and answers with Office 2010 files""",

    'description': """
        Tests questions and answers with Office 2010 files
    """,

    'author': "Jorge Soto Garcia",
    'website': "https://github.com/sotogarcia",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'academy_tests',
    ],

    # always loaded
    'data': [
        'data/at_topic_data.xml',
        'data/at_category_data.xml',
        'data/at_tag_data.xml',
        'data/ir_attachment_data.xml',

        'data/docx_st101_advs_data.xml',
        'data/docx_st102_advs_data.xml',
        'data/docx_st103_advs_data.xml',
        'data/docx_st104_advs_data.xml',
        'data/docx_st105_advs_data.xml',
        'data/docx_st106_advs_data.xml',
        'data/docx_st107_advs_data.xml',
        'data/docx_st108_advs_data.xml',
        'data/docx_st109_advs_data.xml',
        'data/docx_st110_advs_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'js': [
    ],
    'css': [
    ],
}

