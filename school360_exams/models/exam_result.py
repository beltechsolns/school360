from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ExamResult(models.Model):
    _name = "exam.result"
    _inherit = ['school360_base.thread.mixin']
    _description = "Exam Result"
    _order = "exam_id, student_id"

    student_id = fields.Many2one("student.student", string="Student", required=True)
    exam_id = fields.Many2one("exam.exam", string="Exam", required=True)
    marks_obtained = fields.Float(string="Marks Obtained", required=True)
    grade = fields.Selection([('A','A'),('B','B'),('C','C'),('D','D'),('F','F')],
                             string="Grade", compute="_compute_grade", store=True)
    remarks = fields.Text(string="Remarks")
    company_id = fields.Many2one("res.company", string="School", related="exam_id.company_id", store=True)
    academic_year_id = fields.Many2one("school360_base.academic.year", string="Academic Year", related="exam_id.academic_year_id", store=True)
    grade_id = fields.Many2one("school360_academic.grade", string="Grade", related="exam_id.grade_id", store=True)
    section_id = fields.Many2one("school360_academic.section", string="Section", related="exam_id.section_id", store=True)
    subject_id = fields.Many2one("school360_academic.subject", string="Subject", related="exam_id.subject_id", store=True)

    _sql_constraints = [
        ('unique_student_exam', 'unique(student_id, exam_id)', 'This student already has a result for this exam.')
    ]


    @api.depends('marks_obtained')
    def _compute_grade(self):
        for rec in self:
            if rec.marks_obtained >= 90:
                rec.grade = 'A'
            elif rec.marks_obtained >= 80:
                rec.grade = 'B'
            elif rec.marks_obtained >= 70:
                rec.grade = 'C'
            elif rec.marks_obtained >= 60:
                rec.grade = 'D'
            else:
                rec.grade = 'F'