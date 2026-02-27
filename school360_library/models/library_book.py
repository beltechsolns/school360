from odoo import models, fields, api

class LibraryBook(models.Model):
    _name = "library.book"
    _inherit = ['school360_base.thread.mixin']
    _description = "Library Book"
    _rec_name = "name"

    name = fields.Char("Title", required=True)
    isbn = fields.Char("ISBN")
    author = fields.Char("Author")
    category_id = fields.Many2one("library.category", required=True)
    edition = fields.Char()
    description = fields.Text(string="Description")
    book_type = fields.Selection([
        ("physical", "Physical"),
        ("digital", "Digital"),
    ], default="physical", required=True)

    copy_ids = fields.One2many("library.copy", "book_id")
    total_copies = fields.Integer(
        compute="_compute_copies",
        store=True
    )
    available_copies = fields.Integer(
        compute="_compute_copies",
        store=True
    )

    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True
    )

    @api.depends("copy_ids.status")
    def _compute_copies(self):
        for rec in self:
            rec.total_copies = len(rec.copy_ids)
            rec.available_copies = len(
                rec.copy_ids.filtered(lambda c: c.status == "available")
            )