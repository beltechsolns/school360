from odoo import models, fields

class AcademicSubject(models.Model):
    _name = 'school360_academic.subject'
    _description = 'Academic Subject'
    _inherit = ['school360_base.thread.mixin']

    name = fields.Char(string='Subject Name', required=True)
    code = fields.Char(string='Short Code')
    grade_id = fields.Many2one('school360_academic.grade', string='Grade')
    section_id = fields.Many2one('school360_academic.section', string='Section')
    teacher_ids = fields.Many2many('hr.employee', string='Assigned Teachers')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    credits = fields.Float(string='Credits', default=1.0)