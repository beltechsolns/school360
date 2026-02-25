{
    'name': 'School360 Admission',
    'version': '1.0',
    'category': 'Education',
    'summary': 'Student Admission for School360 ERP',
    'description': 'School360 Admission Module',
    'author': 'beltechsolns',
    'license': 'LGPL-3',
    'depends': [
        'school360_base', 'school360_academic', 'mail', 'portal',
    ],
    'data': [
        'security/security_rules.xml',
        'security/ir.model.access.csv',
        'views/student_admission_view.xml',
        'views/admission_attachment_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
    'sequence': 5,
}
