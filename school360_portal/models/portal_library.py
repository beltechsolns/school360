from odoo import models, fields, api

class PortalLibrary(models.Model):
    _name = 'portal.library'
    _description = 'Portal Library'

    student_id = fields.Many2one('student.student')
    book_id = fields.Many2one('school360_library.book')
    due_date = fields.Date()
    fine_amount = fields.Float()

    @api.model
    def get_borrowed_books(self, student_id):
        return self.env['school360_library.borrow'].search([('student_id','=',student_id)])