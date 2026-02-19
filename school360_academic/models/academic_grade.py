from odoo import models, fields

class AcademicGrade(models.Model):
    _name = 'school360_academic.grade'
    _description = 'Academic Grade/Level'
    _inherit = ['school360_base.thread.mixin']

    name = fields.Char(string='Grade Name', required=True)
    code = fields.Char(string='Code')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    section_ids = fields.One2many('school360_academic.section', 'grade_id', string='Sections')
    active = fields.Boolean(default=True)