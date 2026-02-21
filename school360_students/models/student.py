# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


class StudentStudent(models.Model):
    _name = 'student.student'
    _description = 'Student'
    _inherit = ['school360_base.thread.mixin']
    _order = 'name'
    _rec_name = 'name'

    name = fields.Char(
        string='Full Name', required=True, tracking=True,
    )
    student_id = fields.Char(
        string='Student ID', readonly=True, copy=False,
        help="Unique Student ID (generated via company-aware sequence)",
    )
    admission_number = fields.Char(
        string='Admission Number', readonly=True, copy=False,
        help="Admission number (company-aware sequence)",
    )
    admission_id = fields.Many2one(
        'res.partner', string='Admission Record', readonly=True,
        help="Linked admission record if applicable"
    )
    partner_id = fields.Many2one(
        'res.partner', string='Contact', required=True, tracking=True,
        help="Link to res.partner (contacts)",
    )
    date_of_birth = fields.Date(
        string='Date of Birth', required=True, tracking=True,
    )
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender', required=True, default='male', tracking=True)

    company_id = fields.Many2one(
        'res.company', string='School', required=True,
        default=lambda self: self.env.company, tracking=True, index=True,
    )

    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('transferred', 'Transferred'),
        ('graduated', 'Graduated'),
        ('dropped', 'Dropped'),
    ], string='Status', default='draft', required=True, tracking=True)

    enrollment_ids = fields.One2many(
        'student.enrollment', 'student_id', string='Enrollment History',
        help="Links to student.enrollment (historical records)",
    )
    guardian_line_ids = fields.One2many(
        'student.guardian', 'student_id', string='Guardians',
        help="Guardian/parent relationships with relation type",
    )
    guardian_ids = fields.Many2many(
        'res.partner', string='Guardian Partners',
        compute='_compute_guardian_ids', store=True,
    )

    grade_id = fields.Char(string='Current Grade', tracking=True)
    section_id = fields.Char(string='Current Section', tracking=True)

    photo = fields.Binary(string='Photo')
    notes = fields.Text(string='Notes')

    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    enrollment_count = fields.Integer(
        string='Enrollment Count',
        compute='_compute_enrollment_count', store=True,
    )
    guardian_count = fields.Integer(
        string='Guardian Count',
        compute='_compute_guardian_count', store=True,
    )

    _sql_constraints = [
        ('student_id_company_uniq',
         'UNIQUE(student_id, company_id)',
         'Student ID must be unique per company!'),
        ('admission_number_company_uniq',
         'UNIQUE(admission_number, company_id)',
         'Admission Number must be unique per company!'),
    ]

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.date_of_birth:
                dob = rec.date_of_birth
                rec.age = today.year - dob.year - (
                    (today.month, today.day) < (dob.month, dob.day)
                )
            else:
                rec.age = 0

    @api.depends('enrollment_ids')
    def _compute_enrollment_count(self):
        for rec in self:
            rec.enrollment_count = len(rec.enrollment_ids)

    @api.depends('guardian_line_ids')
    def _compute_guardian_ids(self):
        for rec in self:
            rec.guardian_ids = rec.guardian_line_ids.guardian_id

    @api.depends('guardian_line_ids')
    def _compute_guardian_count(self):
        for rec in self:
            rec.guardian_count = len(rec.guardian_line_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('student_id'):
                vals['student_id'] = (
                    self.env['ir.sequence'].next_by_code('school360_base.student') or '/'
                )
            if not vals.get('admission_number'):
                vals['admission_number'] = (
                    self.env['ir.sequence'].next_by_code('school360_base.admission') or '/'
                )
        return super().create(vals_list)

    def write(self, vals):
        if 'status' in vals:
            self._validate_status_transition(vals['status'])
        return super().write(vals)

    _ALLOWED_TRANSITIONS = {
        'draft': ['active'],
        'active': ['transferred', 'graduated', 'dropped'],
        'transferred': [],
        'graduated': [],
        'dropped': [],
    }

    def _validate_status_transition(self, new_status):
        for rec in self:
            allowed = self._ALLOWED_TRANSITIONS.get(rec.status, [])
            if new_status not in allowed:
                raise ValidationError(_(
                    "Cannot transition from '%(current)s' to '%(new)s'. "
                    "Allowed: %(allowed)s",
                    current=rec.status,
                    new=new_status,
                    allowed=', '.join(allowed) or 'none',
                ))

    def action_activate(self):
        self.write({'status': 'active'})

    def action_transfer(self):
        self.write({'status': 'transferred'})

    def action_graduate(self):
        self.write({'status': 'graduated'})

    def action_drop(self):
        self.write({'status': 'dropped'})

    def action_promote(self, new_grade=None, new_section=None, new_year=None):
        self.ensure_one()
        if not all([new_grade, new_year]):
            return False
            
        self.env['student.enrollment'].create({
            'student_id': self.id,
            'academic_year_id': new_year.id if hasattr(new_year, 'id') else new_year,
            'grade_id': new_grade,
            'section_id': new_section or self.section_id,
            'status': 'active',
        })
        
        self.write({
            'grade_id': new_grade,
            'section_id': new_section or self.section_id,
        })
        return True

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        ICP = self.env['ir.config_parameter'].sudo()
        min_age = int(ICP.get_param('school360_base.min_admission_age', '3'))
        max_age = int(ICP.get_param('school360_base.max_admission_age', '25'))

        today = date.today()
        for rec in self:
            if rec.status == 'draft' or not rec.date_of_birth:
                continue
            dob = rec.date_of_birth
            age = today.year - dob.year - (
                (today.month, today.day) < (dob.month, dob.day)
            )
            if age < min_age or age > max_age:
                raise ValidationError(_(
                    "Student age must be between %(min)d and %(max)d years. "
                    "Current age: %(age)d years",
                    min=min_age, max=max_age, age=age,
                ))

    @api.constrains('guardian_line_ids')
    def _check_guardian_mandatory(self):
        mandatory = self.env['ir.config_parameter'].sudo().get_param(
            'school360_base.guardian_mandatory', 'False'
        )
        if mandatory == 'True':
            for rec in self:
                if rec.status == 'active' and not rec.guardian_line_ids:
                    raise ValidationError(_(
                        "At least one guardian is required for active students."
                    ))

    def action_view_guardians(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Guardians'),
            'res_model': 'res.partner',
            'view_mode': 'kanban,list,form',
            'domain': [('id', 'in', self.guardian_ids.ids)],
            'context': {'default_is_company': False},
        }

    def action_view_enrollments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Enrollments'),
            'res_model': 'student.enrollment',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id},
        }
