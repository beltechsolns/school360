from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AcademicTerm(models.Model):
    _name = 'school360_academic.term'
    _description = 'Academic Term'
    _inherit = ['school360_base.thread.mixin']

    name = fields.Char(string='Term Name', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    academic_year_id = fields.Many2one('school360_base.academic.year', string='Academic Year', required=True, ondelete='cascade')
    company_id = fields.Many2one('res.company', related='academic_year_id.company_id', store=True)
    active = fields.Boolean(default=True)

    @api.constrains('start_date', 'end_date', 'academic_year_id')
    def _check_dates(self):
        for rec in self:
            if rec.start_date >= rec.end_date:
                raise ValidationError(_("Term Start Date must be before End Date."))
            if rec.start_date < rec.academic_year_id.start_date or rec.end_date > rec.academic_year_id.end_date:
                raise ValidationError(_("Term dates must be within the Academic Year range (%s to %s).") % 
                                    (rec.academic_year_id.start_date, rec.academic_year_id.end_date))