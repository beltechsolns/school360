{
    'name': 'School360 Portal',
    'version': '1.0',
    'category': 'Education/Portal',
    'summary': 'Self-service portal for students and parents',
    'description': """
        Portal for students and parents to view profiles, attendance, fees, library, and announcements.
    """,
    'author': 'Beltech solutions',
    'website': 'http://school360.local',
    'depends': [
        'school360_base',
        'school360_students',
        'school360_academic',
        'school360_attendance',
        'school360_library',
        'school360_admission',
        "hr"
    ],
    'data': [
        'security/portal_security.xml',
        'security/ir.model.access.csv',
        'views/portal_dashboard.xml',
        'views/portal_attendance.xml',
        'views/portal_fees.xml',
        'views/portal_library.xml',
        'views/portal_admission.xml',
        'views/portal_my_students.xml',
        'views/portal_student_profile.xml'
    ],
    'application': False,
    'installable': True,
}