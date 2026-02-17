from odoo import models, fields, api, _

class AcademicTimetable(models.Model):
    _name = 'school360.academic.timetable'
    _description = 'Basic Timetable'

    name = fields.Char(string='Reference', compute='_compute_name', store=True)
    day_of_week = fields.Selection([
        ('0', 'Monday'), ('1', 'Tuesday'), ('2', 'Wednesday'),
        ('3', 'Thursday'), ('4', 'Friday'), ('5', 'Saturday'), ('6', 'Sunday')
    ], string='Day of Week', required=True)
    
    start_time = fields.Float(string='Start Time', required=True, help="Format: 24h (e.g., 8.5 = 8:30 AM)")
    end_time = fields.Float(string='End Time', required=True)
    
    grade_id = fields.Many2one('school360.academic.grade', string='Grade', required=True)
    section_id = fields.Many2one('school360.academic.section', string='Section', required=True,
                                domain="[('grade_id', '=', grade_id)]")
    subject_id = fields.Many2one('school360.academic.subject', string='Subject', required=True)
    teacher_id = fields.Many2one('res.partner', string='Teacher')
    company_id = fields.Many2one('res.company', related='grade_id.company_id', store=True)

    @api.depends('day_of_week', 'subject_id', 'section_id')
    def _compute_name(self):
        for rec in self:
            day = dict(self._fields['day_of_week'].selection).get(rec.day_of_week)
            rec.name = f"{rec.subject_id.name or ''} - {rec.section_id.name or ''} ({day or ''})"