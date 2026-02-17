from odoo import models, fields

class AcademicSubject(models.Model):
    _name = 'school360.academic.subject'
    _description = 'Academic Subject'

    name = fields.Char(string='Subject Name', required=True)
    code = fields.Char(string='Code')
    grade_id = fields.Many2one('school360.academic.grade', string='Grade')
    teacher_ids = fields.Many2many('res.partner', string='Teachers')
    company_id = fields.Many2one(
        'res.company', 
        string='School', 
        default=lambda self: self.env.company
    )