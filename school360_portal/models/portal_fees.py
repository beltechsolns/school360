from odoo import models, fields, api

class PortalFees(models.Model):
    _name = 'portal.fees'
    _description = 'Portal Fees'
    _auto = False

    student_id = fields.Many2one('student.student', string="Student", required=True)
    fee_id = fields.Many2one('school360.fees', string="Fee")

    currency_id = fields.Many2one(
        'res.currency',
        related='fee_id.currency_id',
        store=True,
        string='Currency'
    )

    amount_due = fields.Monetary(
        related='fee_id.amount_due',
        string="Amount Due",
        store=True,
        currency_field='currency_id'
    )
    amount_paid = fields.Monetary(
        related='fee_id.amount_paid',
        string="Amount Paid",
        store=True,
        currency_field='currency_id'
    )
    state = fields.Selection(related='fee_id.state', string="Status", store=True)
    payment_ids = fields.One2many(related='fee_id.payment_ids', string="Payments")

    @api.model
    def get_student_fees(self, student_id):
        """Fetch all fees and payments for a given student"""
        fees = self.env['school360.fees'].search([('student_id', '=', student_id)])
        return fees