from odoo import models, fields


class SchoolFeesPayment(models.Model):
    _name = 'school360.fees.payment'
    _inherit = ['school360_base.thread.mixin']
    _description = 'Fee Payment'
    _order = 'payment_date desc'

    fee_id = fields.Many2one(
        'school360.fees',
        required=True,
        ondelete='cascade'
    )

    payment_date = fields.Date(default=fields.Date.context_today)
    amount = fields.Monetary(required=True)

    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('bank', 'Bank'),
        ('telebirr', 'TeleBirr'),
    ])

    company_id = fields.Many2one(
        'res.company',
        string='School',
        related='fee_id.company_id',
        store=True
    )

    currency_id = fields.Many2one(
        'res.currency',
        related='fee_id.currency_id',
        store=True
    )