from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Academic Settings
    academic_year_id = fields.Many2one(
        'academic.year',
        string='Current Academic Year',
        config_parameter='school360.academic_year_id'
    )
    grading_system = fields.Selection([
        ('percent', 'Percentage'),
        ('gpa', 'GPA'),
        ('custom', 'Custom')
    ], string='Grading System', config_parameter='school360.grading_system', default='percent')

    attendance_tracking = fields.Boolean(
        string='Enable Attendance Tracking',
        config_parameter='school360.attendance_tracking'
    )

    # Student Settings
    auto_gen_student_id = fields.Boolean(string='Auto Generate Student ID',
                                         config_parameter='school360.auto_gen_student_id')
    guardian_mandatory = fields.Boolean(string='Guardian Mandatory', config_parameter='school360.guardian_mandatory')
    min_admission_age = fields.Integer(string='Minimum Admission Age', config_parameter='school360.min_admission_age')
    max_admission_age = fields.Integer(string='Maximum Admission Age', config_parameter='school360.max_admission_age')

    # Finance Settings
    enable_late_fees = fields.Boolean(string='Enable Late Fees', config_parameter='school360.enable_late_fees')
    late_fee_type = fields.Selection([
        ('fixed', 'Fixed'),
        ('percent', 'Percentage')
    ], string='Late Fee Type', config_parameter='school360.late_fee_type')
    auto_validate_invoices = fields.Boolean(string='Auto Validate Student Invoices',
                                            config_parameter='school360.auto_validate_invoices')

    # Operational Settings
    enable_parent_portal = fields.Boolean(string='Enable Parent Portal',
                                          config_parameter='school360.enable_parent_portal')
    academic_mode = fields.Selection([
        ('school', 'School'),
        ('college', 'College'),
        ('university', 'University')
    ], string='Academic Structure Mode', config_parameter='school360.academic_mode', default='school')