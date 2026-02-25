from odoo import models, fields


class AcademicSection(models.Model):
    _inherit = 'school360_academic.section'

    # This injects the field into the Academic model only when Students is installed
    student_ids = fields.One2many(
        'student.student',
        'section_id',
        string="Students"
    )


class AcademicGrade(models.Model):
    _inherit = 'school360_academic.grade'

    # This injects the field into the Academic model only when Students is installed
    student_ids = fields.One2many(
        'student.student',
        'grade_id',
        string="Students"
    )
