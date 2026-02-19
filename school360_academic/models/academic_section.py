from odoo import models, fields

class AcademicSection(models.Model):
    _name = 'school360_academic.section'
    _description = 'Grade Section'
    _inherit = ['school360_base.thread.mixin']

    name = fields.Char(string='Section Name', required=True)
    grade_id = fields.Many2one('school360_academic.grade', string='Grade', required=True, ondelete='cascade')
    company_id = fields.Many2one('res.company', related='grade_id.company_id', store=True)
    class_teacher_id = fields.Many2one('hr.employee', string='Class Teacher')
    active = fields.Boolean(default=True)