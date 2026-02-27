from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ExamExam(models.Model):
    _name = "exam.exam"
    _description = "Exam"
    _inherit = ['school360_base.thread.mixin']

    name = fields.Char(string="Exam Name", required=True)
    exam_type = fields.Selection([
        ('midterm', 'Midterm'),
        ('final', 'Final'),
        ('semester', 'Semester'),
        ('custom', 'Custom')
    ], string="Exam Type", required=True)
    academic_year_id = fields.Many2one("school360_base.academic.year", string="Academic Year", required=True)
    grade_id = fields.Many2one("school360_academic.grade", string="Grade", required=True)
    section_id = fields.Many2one("school360_academic.section", string="Section")
    subject_id = fields.Many2one("school360_academic.subject", string="Subject")
    result_ids = fields.One2many(
        "exam.result",
        "exam_id",
        string="Student Results"
    )
    exam_date = fields.Date(string="Exam Date", required=True)
    company_id = fields.Many2one("res.company", string="School", required=True)
    notes = fields.Text(string="Notes")

    @api.constrains('exam_date', 'academic_year_id')
    def _check_exam_date(self):
        for rec in self:
            if rec.academic_year_id and rec.exam_date:
                start_date = rec.academic_year_id.start_date
                end_date = rec.academic_year_id.end_date
                if rec.exam_date < start_date or rec.exam_date > end_date:
                    raise ValidationError("Exam date must be within the academic year.")