# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class StudentEnrollment(models.Model):
    _name = 'student.enrollment'
    _description = 'Student Enrollment'
    _inherit = ['school360_base.thread.mixin']
    _order = 'enrollment_date desc, id desc'
    _rec_name = 'display_name'

    student_id = fields.Many2one(
        'student.student', string='Student', required=True,
        ondelete='cascade', tracking=True, index=True,
    )
    academic_year_id = fields.Many2one(
        'school360_base.academic.year', string='Academic Year',
        required=True, tracking=True,
    )

    grade_id = fields.Char(string='Grade', required=True, tracking=True)
    section_id = fields.Char(string='Section', required=True, tracking=True)

    enrollment_date = fields.Date(
        string='Enrollment Date', required=True,
        default=fields.Date.today, 
        tracking=True,
    )
    graduation_date = fields.Date(
        string='Graduation/Transfer Date', tracking=True,
    )

    status = fields.Selection([
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('transferred', 'Transferred'),
        ('dropped', 'Dropped'),
    ], string='Status', default='active', required=True, tracking=True)

    company_id = fields.Many2one(
        'res.company', string='School', required=True,
        default=lambda self: self.env.company, tracking=True, index=True,
    )
    notes = fields.Text(string='Notes')

    student_name = fields.Char(
        related='student_id.name', string='Student Name', store=True,
    )
    student_number = fields.Char(
        related='student_id.student_id', string='Student Number', store=True,
    )

    @api.depends('student_id.name', 'academic_year_id.name', 'grade_id')
    def _compute_display_name(self):
        for rec in self:
            parts = [
                rec.student_id.name or '',
                rec.academic_year_id.name or '',
                rec.grade_id or '',
            ]
            rec.display_name = ' / '.join(filter(None, parts)) or _('New')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self._validate_no_overlap(vals)
        records = super().create(vals_list)
        for rec in records.filtered(lambda r: r.status == 'active'):
            rec.student_id.write({
                'grade_id': rec.grade_id,
                'section_id': rec.section_id,
            })
        return records

    def write(self, vals):
        if 'status' in vals:
            self._validate_status_transition(vals['status'])
            if vals['status'] in ('completed', 'transferred', 'dropped'):
                vals.setdefault('graduation_date', fields.Date.today())

        res = super().write(vals)

        if vals.get('status') == 'active' or ('grade_id' in vals or 'section_id' in vals):
            for rec in self.filtered(lambda r: r.status == 'active'):
                rec.student_id.write({
                    'grade_id': rec.grade_id,
                    'section_id': rec.section_id,
                })
        return res

    def unlink(self):
        for rec in self:
            if rec.status in ('completed', 'transferred', 'dropped'):
                raise UserError(_(
                    "Cannot delete historical enrollment records. "
                    "Only active enrollments can be deleted."
                ))
        return super().unlink()

    def _validate_no_overlap(self, vals):
        student_id = vals.get('student_id')
        academic_year_id = vals.get('academic_year_id')
        grade_id = vals.get('grade_id')
        if not all([student_id, academic_year_id, grade_id]):
            return
        existing = self.search_count([
            ('student_id', '=', student_id),
            ('academic_year_id', '=', academic_year_id),
            ('grade_id', '=', grade_id),
            ('status', 'in', ['active', 'completed']),
        ])
        if existing:
            student = self.env['student.student'].browse(student_id)
            year = self.env['school360_base.academic.year'].browse(academic_year_id)
            raise ValidationError(_(
                "Student '%(student)s' already has an enrollment for "
                "academic year '%(year)s' in grade '%(grade)s'.",
                student=student.name,
                year=year.name,
                grade=grade_id,
            ))

    _ALLOWED_TRANSITIONS = {
        'active': ['completed', 'transferred', 'dropped'],
        'completed': [],
        'transferred': [],
        'dropped': [],
    }

    def _validate_status_transition(self, new_status):
        for rec in self:
            allowed = self._ALLOWED_TRANSITIONS.get(rec.status, [])
            if new_status not in allowed:
                raise ValidationError(_(
                    "Cannot transition enrollment from '%(current)s' to '%(new)s'. "
                    "Allowed: %(allowed)s",
                    current=rec.status,
                    new=new_status,
                    allowed=', '.join(allowed) or 'none',
                ))

    @api.constrains('enrollment_date', 'graduation_date')
    def _check_dates(self):
        for rec in self:
            if rec.enrollment_date and rec.graduation_date:
                if rec.graduation_date < rec.enrollment_date:
                    raise ValidationError(_(
                        "Graduation/Transfer date cannot be earlier "
                        "than enrollment date."
                    ))

    @api.constrains('academic_year_id', 'enrollment_date')
    def _check_academic_year_dates(self):
        for rec in self:
            ay = rec.academic_year_id
            if ay and rec.enrollment_date and ay.start_date and ay.end_date:
                if not (ay.start_date <= rec.enrollment_date <= ay.end_date):
                    raise ValidationError(_(
                        "Enrollment date must be within the academic year "
                        "period (%(start)s to %(end)s).",
                        start=ay.start_date,
                        end=ay.end_date,
                    ))

    def action_complete(self):
        self.write({'status': 'completed', 'graduation_date': fields.Date.today()})

    def action_transfer(self):
        self.write({'status': 'transferred', 'graduation_date': fields.Date.today()})

    def action_drop(self):
        self.write({'status': 'dropped', 'graduation_date': fields.Date.today()})
