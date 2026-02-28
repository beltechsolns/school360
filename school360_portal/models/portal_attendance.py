from odoo import models, fields, api

class PortalAttendance(models.Model):
    _name = 'portal.attendance'
    _description = 'Portal Attendance'

    student_id = fields.Many2one('student.student')
    attendance_date = fields.Date()
    status = fields.Selection([('present', 'Present'), ('absent', 'Absent')])

    @api.model
    def get_attendance(self, student_id):
        return self.env['school360_attendance.attendance.line'].search([('student_id', '=', student_id)])