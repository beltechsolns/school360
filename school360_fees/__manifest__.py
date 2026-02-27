{
    'name': 'School360 Fees',
    'version': '1.0',
    'category': 'Education',
    'summary': 'Student Fees for School360 ERP',
    'description': 'School360 Fees Module',
    'author': 'beltechsolns',
    'license': 'LGPL-3',
    'depends': [
        'school360_base', 'school360_students', 'school360_academic', 'mail', 'portal',
    ],
    'data': [
        'security/fees_security.xml',
        'security/ir.model.access.csv',
        'views/fee_views.xml',
        'views/fee_structure_views.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
    'sequence': 5,
}
