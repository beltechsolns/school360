from odoo import models, fields

class AcademicGrade(models.Model):
    _name = 'school360_academic.grade'
    _description = 'Academic Grade/Level'
    _inherit = ['school360_base.thread.mixin']

    name = fields.Char(string='Grade Name', required=True)
    code = fields.Char(string='Code')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, readonly=True)
    section_ids = fields.One2many('school360_academic.section', 'grade_id', string='Sections')
    # student_ids=fields.Char(string="Student Id")
    # student_ids = fields.One2many('student.student', 'grade_id', string="Students")
    active = fields.Boolean(default=True)


