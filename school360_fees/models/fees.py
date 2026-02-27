from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Fees(models.Model):
    _name = 'fees.fees'
    _description = 'Student Fees'
    _inherit = ['school360_base.thread.mixin']
    _order = 'payment_date desc'

    payment_reference = fields.Char(string="Payment Reference", compute="_compute_payment_reference", store=True)
    student_id = fields.Many2one('student.student', string="Student", required=True, tracking=True)
    fee_structure_id = fields.Many2one('fees.structure', string="Fee Structure", required=True, tracking=True)

    total_amount = fields.Float(string="Base Amount", related='fee_structure_id.amount', store=True)
    amount_paid = fields.Float(string="Amount Paid", tracking=True)
    net_amount_due = fields.Float(string="Net Due", compute="_compute_totals", store=True)
    amount_remaining = fields.Float(string="Remaining", compute="_compute_totals", store=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('unpaid', 'Unpaid'),
        ('partially_paid', 'Partially Paid'),
        ('paid', 'Paid')
    ], string="Status", compute="_compute_totals", store=True, default='draft')

    # Scholarship & Discounts
    has_discount = fields.Boolean(string="Apply Discount")
    discount_percent = fields.Float(string="Discount %")
    has_scholarship = fields.Boolean(string="Scholarship")
    scholarship_type = fields.Selection([
        ('full', 'Full (100%)'),
        ('half', 'Half (50%)')
    ], string="Scholarship Type")

    payment_date = fields.Date(string="Payment Date", default=fields.Date.context_today)
    payment_method = fields.Selection([
        ('cash', 'Cash'), ('bank', 'Bank'), ('telebirr', 'TeleBirr')
    ], string="Method")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, reaonly=True)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')

    @api.depends('student_id', 'fee_structure_id')
    def _compute_payment_reference(self):
        for rec in self:
            if rec.student_id and rec.fee_structure_id:
                rec.payment_reference = f"{rec.student_id.name} - {rec.fee_structure_id.name}"

    @api.depends('total_amount', 'amount_paid', 'has_discount', 'discount_percent', 'has_scholarship',
                 'scholarship_type')
    def _compute_totals(self):
        for rec in self:
            # 1. Start with Base
            net_due = rec.total_amount

            # 2. Scholarship Logic
            if rec.has_scholarship:
                if rec.scholarship_type == 'full':
                    net_due = 0
                elif rec.scholarship_type == 'half':
                    net_due *= 0.5

            # 3. Discount Logic (applied to the amount after scholarship)
            if rec.has_discount and rec.discount_percent > 0:
                net_due -= (net_due * (rec.discount_percent / 100))

            rec.net_amount_due = net_due
            rec.amount_remaining = net_due - rec.amount_paid

            # 4. State Management
            if rec.amount_paid <= 0:
                rec.state = 'unpaid'
            elif rec.amount_remaining <= 0:
                rec.state = 'paid'
            else:
                rec.state = 'partially_paid'

    @api.constrains('amount_paid')
    def _check_overpayment(self):
        for rec in self:
            if rec.amount_paid > rec.net_amount_due:
                raise ValidationError("Amount paid cannot exceed the Net Due amount.")
