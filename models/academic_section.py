from odoo import models, fields

class AcademicSection(models.Model):
    _name = 'school360.academic.section'
    _description = 'Academic Section'

    name = fields.Char(string='Section Name', required=True)
    
    grade_id = fields.Many2one(
        'school360.academic.grade', 
        string='Grade', 
        required=True, 
        ondelete='cascade'
    )
    
    company_id = fields.Many2one(
        'res.company', 
        string='School',
        related='grade_id.company_id', 
        store=True, 
        readonly=True
    )
    
    class_teacher_id = fields.Many2one('res.partner', string='Class Teacher')