from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class LibraryBorrow(models.Model):
    _name = "library.borrow"
    _inherit = ['school360_base.thread.mixin']
    _description = "Library Borrow Record"

    borrower_type = fields.Selection([
        ("student", "Student"),
        ("staff", "Staff")
    ], required=True)

    borrower_student_id = fields.Many2one("student.student")
    borrower_employee_id = fields.Many2one("hr.employee")

    book_copy_id = fields.Many2one("library.copy", required=True)

    borrow_date = fields.Date(default=fields.Date.today)
    due_date = fields.Date()
    return_date = fields.Date()

    status = fields.Selection([
        ("borrowed", "Borrowed"),
        ("returned", "Returned"),
        ("overdue", "Overdue"),
    ], default="borrowed")

    fine_amount = fields.Float()

    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True
    )

    @api.constrains("book_copy_id")
    def _check_copy_availability(self):
        for rec in self:
            if rec.book_copy_id.status != "available":
                raise ValidationError("This book copy is not available.")