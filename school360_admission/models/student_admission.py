from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class StudentAdmission(models.Model):
    _name = "student.admission"
    _description = 'Student Admission'
    _inherit = ['school360_base.thread.mixin']
    _order = "application_date desc"

    name = fields.Char(string="Applicant Name", required=True, tracking=True)
    applicant_partner_id = fields.Many2one('res.partner', string="Existing Contact")
    date_of_birth = fields.Date(string="Date of Birth", required=True, tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], tracking=True)

    admission_number = fields.Char(string="Admission No.", readonly=True, copy=False, default=lambda self: _('New'))
    student_id = fields.Char(string="Student ID", readonly=True, copy=False)
    company_id = fields.Many2one('res.company', string="Company/School", default=lambda self: self.env.company,
                                 required=True)

    status = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('verified', 'Verified'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ], default='draft', tracking=True, index=True)

    grade_id = fields.Many2one('school360_academic.grade', string="Grade", required=True)
    section_id = fields.Many2one('school360_academic.section', string="Section")
    academic_year_id = fields.Many2one('school360_base.academic.year', string="Academic Year", required=True)

    guardian_ids = fields.Many2many('res.partner', string="Guardians")
    attachment_ids = fields.One2many('student.admission.attachment', 'admission_id', string="Attachments")

    notes = fields.Text(string="Remarks")
    application_date = fields.Date(string="Submission Date", default=fields.Date.today)
    decision_date = fields.Date(string="Decision Date", readonly=True)

    # Constraints & Validations
    @api.constrains('date_of_birth', 'guardian_ids', 'name', 'academic_year_id', 'company_id')
    def _check_admission_policy(self):
        params = self.env['ir.config_parameter'].sudo()

        min_age = int(params.get_param('school360.min_admission_age', default=0))
        max_age = int(params.get_param('school360.max_admission_age', default=100))
        guardian_required = params.get_param('school360.guardian_mandatory')

        for rec in self:
            # Age Validation
            if rec.date_of_birth:
                age = relativedelta(fields.Date.today(), rec.date_of_birth).years
                if age < min_age or age > max_age:
                    raise ValidationError(
                        _("Age Error: Applicant is %s years old. Allowed range: %s-%s.") % (age, min_age, max_age))

            # Mandatory Guardian Check
            if guardian_required and not rec.guardian_ids:
                raise ValidationError(_("Policy Violation: At least one guardian is required for admission."))

            # Uniqueness: One active admission per applicant/year/company
            duplicates = self.search_count([
                ('id', '!=', rec.id),
                ('name', '=', rec.name),
                ('date_of_birth', '=', rec.date_of_birth),
                ('academic_year_id', '=', rec.academic_year_id.id),
                ('company_id', '=', rec.company_id.id),
                ('status', 'not in', ['rejected'])
            ])
            if duplicates > 0:
                raise ValidationError(
                    _("Constraint: An active application already exists for this applicant in this academic year."))

    # Workflow Automations
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('admission_number', _('New')) == _('New'):
                comp_id = vals.get('company_id') or self.env.company.id
                vals['admission_number'] = self.env['ir.sequence'].with_company(comp_id).next_by_code(
                    'school360.admission') or _('New')
        return super().create(vals_list)

    def action_submit(self):
        self.write({'status': 'submitted'})

    def action_verify(self):
        # 5.4 Required Attachments Rule
        for rec in self:
            if not rec.attachment_ids:
                raise ValidationError(_("Verification Denied: Required attachments are missing."))
        self.write({'status': 'verified'})

    def action_accept(self):
        for record in self:
            if record.status == 'accepted':
                continue

            # 1. Partner Logic (Existing or Create New)
            partner = record.applicant_partner_id
            if not partner:
                partner = self.env['res.partner'].create({
                    'name': record.name,
                    'is_company': False,
                    'type': 'contact',
                    'email': record.guardian_ids[0].email if record.guardian_ids else False,
                })

            #  Generate Student ID
            student_id_val = self.env['ir.sequence'].with_company(record.company_id).next_by_code('school360.student')

            # Create Record in school360_students
            self.env['student.student'].create({
                'name': record.name,
                'partner_id': partner.id,
                'date_of_birth': record.date_of_birth,
                'gender': record.gender,
                'grade_id': record.grade_id.id,
                'section_id': record.section_id.id if record.section_id else False,
                'company_id': record.company_id.id,
                'admission_number': record.admission_number,
                'student_id': student_id_val,
                'guardian_line_ids': [(0, 0, {'guardian_id': g.id}) for g in record.guardian_ids]
            })

            record.write({
                'student_id': student_id_val,
                'status': 'accepted',
                'decision_date': fields.Date.today()
            })

    def action_reject(self):
        self.write({'status': 'rejected', 'decision_date': fields.Date.today()})
