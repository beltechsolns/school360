from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AcademicTerm(models.Model):
    _name = 'school360.academic.term'
    _description = 'Academic Term'
    _order = 'start_date'

    name = fields.Char(string='Term Name', required=True)
    
    academic_year_id = fields.Many2one(
        'school360.academic.year',
        string='Academic Year',
        required=True,
        ondelete='cascade'
    )

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)

    # Active flag to allow archiving/unarchiving records
    active = fields.Boolean(string='Active', default=True)

    company_id = fields.Many2one(
        'res.company',
        related='academic_year_id.company_id',
        store=True,
        readonly=True
    )

    @api.constrains('start_date', 'end_date', 'academic_year_id')
    def _check_dates(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                if rec.start_date >= rec.end_date:
                    raise ValidationError(
                        _("Term Start Date must be before End Date.")
                    )

            if rec.academic_year_id:
                year = rec.academic_year_id
                if rec.start_date < year.start_date or rec.end_date > year.end_date:
                    raise ValidationError(
                        _("Term must be within the Academic Year range.")
                    )
