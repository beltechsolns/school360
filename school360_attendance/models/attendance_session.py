from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AttendanceSession(models.Model):
    _name = "attendance.session"
    _inherit = ['school360_base.thread.mixin']
    _description = "Attendance Session"

    date = fields.Date(string="Attendance Date", required=True)
    academic_year_id = fields.Many2one('school360_base.academic.year', string="Academic Year", required=True)
    grade_id = fields.Many2one('school360_academic.grade', string="Grade", required=True)
    section_id = fields.Many2one('school360_academic.section', string="Section", required=True)
    subject_id = fields.Many2one('school360_academic.subject', string="Subject")
    teacher_id = fields.Many2one('hr.employee', string="Teacher")
    period_number = fields.Integer(string="Period Number", required=True)
    start_time = fields.Float(string="Start Time")
    end_time = fields.Float(string="End Time")
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed')], default='draft', string="Status")
    company_id = fields.Many2one('res.company', string="School", required=True)

    line_ids = fields.One2many('attendance.line', 'session_id', string="Attendance Lines")

    _sql_constraints = [
        ('unique_session', 'unique(date, grade_id, section_id, period_number, company_id)',
         'Attendance session already exists for this period.'),
    ]

    @api.constrains('line_ids')
    def _check_lines(self):
        for session in self:
            if session.state == 'confirmed' and not session.line_ids:
                raise ValidationError("Cannot confirm a session without attendance lines.")