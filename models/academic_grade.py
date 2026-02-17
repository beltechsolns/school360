from odoo import models, fields

class AcademicGrade(models.Model):
    _name = 'school360.academic.grade'
    _description = 'Academic Grade'

    name = fields.Char(string='Grade Name', required=True)
    code = fields.Char(string='Code')
    
    company_id = fields.Many2one(
        'res.company', 
        string='School', 
        required=True, 
        default=lambda self: self.env.company
    )
    
    section_ids = fields.One2many('school360.academic.section', 'grade_id', string='Sections')