from odoo import models, fields, api


class PortalAdmission(models.Model):
    _name = 'portal.admission'
    _description = 'Portal Admission'

    student_id = fields.Many2one('student.student')
    application_status = fields.Selection([('draft', 'Draft'), ('submitted', 'Submitted'), ('approved', 'Approved')])

    @api.model
    def get_application_status(self, student_id):
        return self.env['school360_admission.application'].search([('student_id', '=', student_id)])