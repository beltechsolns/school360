# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StudentGuardian(models.Model):
    _name = 'student.guardian'
    _description = 'Student–Guardian Relationship'
    _inherit = ['school360_base.thread.mixin']
    # _rec_name = 'guardian_id'

    student_id = fields.Many2one(
        'student.student', string='Student', required=True,
        ondelete='cascade', index=True,
    )
    guardian_id = fields.Many2one(
        'res.partner', string='Guardian', required=True,
        ondelete='restrict',
    )
    relation_type = fields.Selection([
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('guardian', 'Guardian'),
    ], string='Relation', required=True, default='guardian')

    guardian_name = fields.Char(related='guardian_id.name', store=True)
    guardian_email = fields.Char(related='guardian_id.email')
    guardian_phone = fields.Char(related='guardian_id.phone')

    _sql_constraints = [
        ('student_guardian_uniq',
         'UNIQUE(student_id, guardian_id)',
         'This guardian is already linked to this student!'),
    ]
