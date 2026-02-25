# -*- coding: utf-8 -*-
{
    "name": "School360 Base",
    "version": "1.0",
    "summary": "Base module for School360 ERP",
    "description": """
        Foundational module of School360 ERP.
        Provides root menu, security groups, company-aware sequences, 
        and configuration framework.
    """,
    "category": "Education",

    'author': "beltechsolns",
    'website': "https://www.yourcompany.com",

    # any module necessary for this one to work correctly
    "depends": ["base", "mail", "portal"],

    "sequence": '10',

    'data': [
        # Security
        'security/school360_base_security_groups.xml',
        'security/ir.model.access.csv',
        'security/school360_base_record_rules.xml',

        # Actions
        'views/school360_base_academic_year_views.xml',
        'views/school360_base_res_config_settings.xml',

        # Menus
        'views/school360_base_menu_views.xml',

        # Data
        'data/student_id_sequence.xml',
        'data/admission_number_sequence.xml',
    ],

    'license': 'LGPL-3',
    "installable": True,
    "application": True,
    "auto_install": False,
}
