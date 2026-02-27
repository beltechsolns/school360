{
    "name": "School360 Library",
    "version": "1.0",
    "summary": "Library Management for School360",
    "author": "BelTech Solutions",
    "depends": [
        "school360_base",
        "school360_students",
        "hr",
        "portal",
    ],
    "data": [
        "security/library_security.xml",
        "security/ir.model.access.csv",
        "data/sequence.xml",
        "views/library_category_views.xml",
        "views/library_book_views.xml",
        "views/library_copy_views.xml",
        "views/library_borrow_views.xml",
        "views/library_menus.xml",
    ],
    "installable": True,
    "application": True,
}