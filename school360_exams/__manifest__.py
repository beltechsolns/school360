{
    "name": "School360 Exams",
    "version": "1.0",
    "category": "Education",
    "License":"LGPL-3",
    "summary": "Manage exams, results, and student scores",
    "description": """Allows schools to define exams, record student results, and display results on portals.""",
    "depends": ["school360_base", "school360_students", "school360_academic"],
    "data": [
        "security/exam_security.xml",
        "security/ir.model.access.csv",
        "views/exam_views.xml",
        "views/exam_result_views.xml",
        "views/exam_menus.xml"
    ],
    "installable": True,
    "application": False,
}