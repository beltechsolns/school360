{
    'name': 'School360 Fees Management',
    'version': '1.0',
    'category': 'Education',
    'summary': 'Manage Student Fees and Payments',
    'depends': [
        'school360_base', 'school360_students', 'school360_academic', 'mail', 'portal',
    ],
    'data': [
        'security/fees_security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/sequence.xml',
        'views/fee_structure_views.xml',
        'views/fee_payment_views.xml',
        'views/fee_views.xml',
        'views/fee_menus.xml'
    ],
    'installable': True,
    'application': True,
}
