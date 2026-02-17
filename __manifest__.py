# -*- coding: utf-8 -*-
{
    "name": "School360 Academic",
    "version": "1.0",
    "summary": "Core Academic Structure: Terms, Grades, Sections, and Subjects",
    "category": "Education",
    "author": "beltechsolns",
    "depends": ["school360"],
    "data": [
        "security/ir.model.access.csv",
        "security/academic_security.xml",
        "views/academic_year_views.xml",
        "views/academic_term_views.xml",
        "views/academic_grade_views.xml",
        "views/academic_section_views.xml",
        "views/academic_subject_views.xml",
        "views/academic_timetable_views.xml",
        "views/academic_menu_views.xml",
    ],
    "installable": True,
    "application": False,
}