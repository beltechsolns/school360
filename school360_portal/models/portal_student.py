from odoo import models, fields, api

class PortalStudent(models.Model):
    _name = 'portal.student'
    _description = 'Portal Student'

    student_id = fields.Many2one(
        'student.student',
        string='Student',
        required=True
    )


    @api.model
    def get_portal_students(self, user):
        """
        Return all students linked to a portal user via guardians.
        Uses the Many2many 'guardian_ids' field in student.
        """
        return self.env['student.student'].search([
            ('guardian_ids.user_id', '=', user.id)
        ])