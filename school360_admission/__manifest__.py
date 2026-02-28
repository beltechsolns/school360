{
    'name': 'School360 Admission',
    'version': '18.0.1.0.0',
    'category': 'Education',
    'summary': 'Complete student lifecycle management for School360 ERP',
    'description': 'School360 Admission Module',
    'author': '',
    'license': 'LGPL-3',
    'depends': [
        'school360_base', 'school360_academic','school360_students','mail', 'portal',
    ],
    'data': [
        'security/security_rules.xml',
        'security/ir.model.access.csv',
        'views/student_admission_view.xml',
        'views/admission_attachment_view.xml',
        'views/admission_menus.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 10,
}
