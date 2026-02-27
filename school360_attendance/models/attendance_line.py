from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AttendanceLine(models.Model):
    _name = "attendance.line"
    _inherit = ['school360_base.thread.mixin']
    _description = "Attendance Line"

    session_id = fields.Many2one('attendance.session', string="Session", required=True, ondelete='cascade')
    student_id = fields.Many2one('student.student', string="Student", required=True)
    status = fields.Selection([('present','Present'), ('absent','Absent'), ('late','Late'), ('excused','Excused')], default='present')
    remarks = fields.Text(string="Remarks")

    _sql_constraints = [
        ('unique_student_session', 'unique(session_id, student_id)', 'Attendance already recorded for this student in this session.'),
    ]