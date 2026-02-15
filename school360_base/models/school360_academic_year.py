from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AcademicYear(models.Model):
    _name = 'school360_base.academic.year'
    _description = 'Academic Year'
    _inherit = ['school360_base.thread.mixin']
    _order = 'start_date desc, id desc'

    name = fields.Char(string='Name', required=True, help="e.g., 2025-2026")
    code = fields.Char(string='Code', copy=False, help="Short code for reports")
    start_date = fields.Date(string='Start Date', required=True, tracking=True)
    end_date = fields.Date(string='End Date', required=True, tracking=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', index=True, tracking=True, copy=False)

    company_id = fields.Many2one(
        'res.company', string='School', required=True, readonly=True,
        default=lambda self: self.env.company, index=True
    )

    active = fields.Boolean(default=True, help="Archive record instead of deleting.")

    # Constraints & Validations
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for rec in self:
            if rec.start_date >= rec.end_date:
                raise ValidationError(_("Start Date must be before End Date."))

    @api.constrains('start_date', 'end_date', 'company_id')
    def _check_overlap(self):
        for rec in self:
            domain = [
                ('id', '!=', rec.id),
                ('company_id', '=', rec.company_id.id),
                ('start_date', '<=', rec.end_date),
                ('end_date', '>=', rec.start_date),
            ]
            if self.search_count(domain):
                raise ValidationError(_("Dates overlap with an existing Academic Year in this school."))

    # State Management
    def write(self, vals):
        for rec in self:
            if rec.state == 'closed':
                raise ValidationError(_(
                    "This Academic Year is Closed. To prevent data corruption, "
                    "no further edits are allowed on this record."
                ))
        res = super().write(vals)

        if vals.get('state') == 'active':
            self._auto_close_others()
        return res

    def _auto_close_others(self):
        for rec in self:
            others = self.search([
                ('id', '!=', rec.id),
                ('company_id', '=', rec.company_id.id),
                ('state', '=', 'active')
            ])
            if others:
                others.write({'state': 'closed'})

    # Actions
    def action_activate(self):
        self.ensure_one()
        return self.write({
            'state': 'active',
            'active': True,  # unarchive automatically
        })

    @api.constrains('state', 'active')
    def _check_active_archived(self):
        for rec in self:
            if rec.state == 'active' and not rec.active:
                raise ValidationError(
                    _("An Active Academic Year cannot be archived.")
                )

    def action_close(self):
        return self.write({'state': 'closed'})

    # Current active year Resolver
    @api.model
    def get_current_year(self, company_id=None):
        cid = company_id or self.env.company.id
        return self.search([
            ('company_id', '=', cid),
            ('state', '=', 'active'),
            ('active', '=', True),
        ], limit=1)
