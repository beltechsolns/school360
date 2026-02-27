{
    'name': 'School360 Attendance',
    'version': '1.0',
    'summary': 'Period-based student attendance tracking with bulk import',
    'category': 'Education',
    'depends': ['school360_base', 'school360_students', 'school360_academic'],
    'data': [
        'security/attendance_security.xml',
        'security/ir.model.access.csv',
        'views/attendance_session_views.xml',
        'views/attendance_line_views.xml',
        'views/attendance_import_wizard_views.xml',
        'views/attendance_menus.xml'
    ],
    'installable': True,
    'application': False,
}