from odoo import models, fields, api


class AcademicYear(models.Model):
    _name = 'academic.year'
    _description = 'Academic Year'

    name = fields.Char(string='Academic Year', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    state = fields.Selection([
        ('active', 'Active'),
        ('closed', 'Closed'),
    ], string='State', default='active')
    company_id = fields.Many2one(
        'res.company', string='School', default=lambda self: self.env.company, required=True
    )
