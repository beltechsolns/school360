# -*- coding: utf-8 -*-
{
    'name': 'School360 Students',
    'version': '18.0.1.0.0',
    'category': 'Education/School360',
    'summary': 'Complete student lifecycle management for School360 ERP',
    'description': 'School360 Students Module',
    'author': 'Solomon Yitayew',
    'website': 'https://school360.com',
    'license': 'LGPL-3',
    'depends': [
        'school360_base',
        'mail',
        'portal',
    ],
    'data': [
        # Security (order matters: groups → ACL → rules)
        'security/ir.model.access.csv',
        'security/record_rules.xml',

        # Views
        'views/student_dashboard_views.xml',
        'views/student_views.xml',
        'views/enrollment_views.xml',
        'views/student_menu.xml',
        'views/portal_templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'school360_students/static/src/dashboard/dashboard.js',
            'school360_students/static/src/dashboard/dashboard.xml',
            'school360_students/static/src/dashboard/dashboard.scss',
        ],
        'web.assets_frontend': [
            'school360_students/static/src/css/student_portal.css',
            'school360_students/static/src/js/student_portal.js',
        ],
    },
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
    'sequence': 10,
}
