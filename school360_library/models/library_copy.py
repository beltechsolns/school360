from odoo import models, fields, api

class LibraryCopy(models.Model):
    _name = "library.copy"
    _inherit = ['school360_base.thread.mixin']
    _description = "Library Book Copy"

    book_id = fields.Many2one("library.book", required=True,ondelete="cascade")
    copy_number = fields.Char(required=True)
    status = fields.Selection([
        ("available", "Available"),
        ("borrowed", "Borrowed"),
        ("lost", "Lost"),
        ("damaged", "Damaged"),
    ], default="available")

    location = fields.Char("Shelf Location")

    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True
    )