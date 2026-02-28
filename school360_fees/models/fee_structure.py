from odoo import models, fields


class FeesStructure(models.Model):
    _name = 'school360.fees.structure'
    _inherit = ['school360_base.thread.mixin']
    _description = 'Fee Structure'

    name = fields.Char(required=True)
    grade_id = fields.Many2one('school360_academic.grade')
    amount = fields.Monetary(
        string="Amount",
        required=True
    )

    company_id = fields.Many2one(
        'res.company',
        default=lambda self: self.env.company
    )

    currency_id = fields.Many2one(
        'res.currency',
        string='School',
        related='company_id.currency_id',
        store=True
    )

    active = fields.Boolean(default=True)