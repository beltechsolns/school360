{
    'name': 'School360 Dashboard',
    'version': '18.0.1.1',
    "model version": "1.0",
    "author": "BelTech Solutions",
    'summary': 'Dashboard for School360',
    'depends': [
        'base', 
        'web',
        'hr',
        'school360_academic', 
        'school360_students',
        'school360_attendance',
        'school360_fees',
        'school360_library',
    ],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/dashboard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'school360_dashboard/static/src/components/dashboard/dashboard.scss',
            'school360_dashboard/static/src/components/dashboard/dashboard.js',
            'school360_dashboard/static/src/components/dashboard/dashboard.xml',
        ],
    },
    'installable': True,
    'application': True,
}