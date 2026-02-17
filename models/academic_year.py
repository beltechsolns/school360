from odoo import models, fields

class AcademicYear(models.Model):
    _inherit = 'school360.academic.year'

    term_ids = fields.One2many('school360.academic.term', 'academic_year_id', string='Terms')