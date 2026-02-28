from odoo import models, fields, api
from odoo.exceptions import UserError


class SchoolFees(models.Model):
    _name = 'school360.fees'
    _description = 'Student Fee'
    _inherit = ['school360_base.thread.mixin']
    _order = 'id desc'

    name = fields.Char(string="Reference", required=True, copy=False, readonly=True, default='New')
    student_id = fields.Many2one('student.student', required=True, tracking=True)
    structure_id = fields.Many2one('school360.fees.structure', required=True)
    total_amount = fields.Monetary(related='structure_id.amount', store=True)

    # New fields
    discount = fields.Float(string="Discount (%)", default=0.0)
    scholarship = fields.Float(string="Scholarship Amount", default=0.0)

    payment_ids = fields.One2many('school360.fees.payment', 'fee_id', string="Payments")
    amount_paid = fields.Monetary(compute='_compute_amounts', store=True)
    amount_due = fields.Monetary(compute='_compute_amounts', store=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('cancel', 'Cancelled'),
    ], default='draft', tracking=True)

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', store=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('school360.fees.seq')
        return super().create(vals)

    @api.depends('payment_ids.amount', 'discount', 'scholarship')
    def _compute_amounts(self):
        for rec in self:
            base_amount = rec.total_amount
            discount_amount = base_amount * (rec.discount / 100)
            net_amount = base_amount - discount_amount - rec.scholarship

            # Make sure due is not negative
            paid = sum(rec.payment_ids.mapped('amount'))
            rec.amount_paid = paid
            rec.amount_due = max(net_amount - paid, 0)

            # Automatic state update
            if rec.amount_due <= 0 and net_amount > 0:
                rec.state = 'paid'
            elif paid > 0:
                rec.state = 'open'
            else:
                rec.state = 'draft'

    # Button Methods for state changes
    def action_set_open(self):
        for rec in self:
            if rec.state not in ['draft', 'cancel']:
                raise UserError(f"Cannot open fee from state {rec.state}")
            rec.state = 'open'

    def action_set_paid(self):
        for rec in self:
            if rec.state not in ['draft', 'open']:
                raise UserError(f"Cannot mark as paid from state {rec.state}")
            rec.state = 'paid'

    def action_set_cancel(self):
        for rec in self:
            if rec.state not in ['draft', 'open']:
                raise UserError(f"Cannot cancel from state {rec.state}")
            rec.state = 'cancel'

    def action_set_draft(self):
        for rec in self:
            if rec.state != 'cancel':
                raise UserError("Can only reset to draft from cancelled state")
            rec.state = 'draft'