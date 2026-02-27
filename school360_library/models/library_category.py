from odoo import models, fields

class LibraryCategory(models.Model):
    _name = "library.category"
    _inherit = ['school360_base.thread.mixin']
    _description = "Library Book Category"
    _rec_name = "name"

    name = fields.Char(required=True)
    description = fields.Text()
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True
    )