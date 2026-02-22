from odoo import models, fields, api


class AdmissionAttachment(models.Model):
    _name = 'student.admission.attachment'
    _description = 'Admission Attachments'
    _inherit = ['school360_base.thread.mixin']

    admission_id = fields.Many2one('student.admission', string="Admission", ondelete='cascade', tracking=True)
    file = fields.Binary(string="File", required=True, tracking=True)
    description = fields.Char(string="Description", tracking=True)
