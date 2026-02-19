from odoo import models, fields, api

class AcademicTimetable(models.Model):
    _name = 'school360_academic.timetable'
    _description = 'Class Timetable'

    name = fields.Char(string='Reference', compute='_compute_name', store=True)
    day_of_week = fields.Selection([
        ('0', 'Monday'), ('1', 'Tuesday'), ('2', 'Wednesday'),
        ('3', 'Thursday'), ('4', 'Friday'), ('5', 'Saturday'), ('6', 'Sunday')
    ], string='Day', required=True)
    
    start_time = fields.Float(string='Start Time', required=True, help="Format: 8.5 for 8:30")
    end_time = fields.Float(string='End Time', required=True)
    
    grade_id = fields.Many2one('school360_academic.grade', string='Grade', required=True)
    section_id = fields.Many2one('school360_academic.section', string='Section', required=True)
    subject_id = fields.Many2one('school360_academic.subject', string='Subject', required=True)
    teacher_id = fields.Many2one('hr.employee', string='Teacher', required=True)
    company_id = fields.Many2one('res.company', related='grade_id.company_id', store=True)

    @api.depends('day_of_week', 'subject_id', 'section_id')
    def _compute_name(self):
        for rec in self:
            day_name = dict(self._fields['day_of_week'].selection).get(rec.day_of_week)
            rec.name = f"{rec.section_id.name or ''} - {rec.subject_id.name or ''} ({day_name})"