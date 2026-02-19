from odoo import models, fields

class AcademicYear(models.Model):
    _inherit = 'school360_base.academic.year'

    term_ids = fields.One2many('school360_academic.term', 'academic_year_id', string='Terms')