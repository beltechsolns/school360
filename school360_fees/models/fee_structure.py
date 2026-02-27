from odoo import models, fields


class FeeStructure(models.Model):
    _name = 'fees.structure'
    _description = 'Fee Structure'
    _inherit = ['school360_base.thread.mixin']

    name = fields.Char(string='Fee Name', required=True, tracking=True)
    code = fields.Char(string="Code", required=True)
    amount = fields.Float(string="Amount", required=True, tracking=True)

    company_id = fields.Many2one(
        'res.company',
        string="Company",
        default=lambda self: self.env.company,
        readonly=True
    )
    currency_id = fields.Many2one(
        'res.currency',
        related='company_id.currency_id'
    )
