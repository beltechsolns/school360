from odoo import models, api, fields, tools
import logging

_logger = logging.getLogger(__name__)

class SchoolDashboard(models.Model):
    _name = 'school360.dashboard'
    _description = 'Dashboard Data Engine'

    def _safe_search_read(self, model_name, domain, fields):
        """Helper to fetch data only if the model exists in the registry."""
        if model_name in self.env.registry:
            return self.env[model_name].search_read(domain, fields)
        _logger.warning(f"Dashboard: Model {model_name} not found in registry. Skipping.")
        return []

    @api.model
    def get_filter_options(self):
        """Returns lists of records to populate the dashboard filter dropdowns safely."""
        company_id = self.env.company.id
        domain = [('company_id', '=', company_id)]
        
        years = self._safe_search_read('school360.academic.year', domain, ['id', 'name'])
        if not years:
            years = self._safe_search_read('school360_academic.year', domain, ['id', 'name'])

        return {
            "years": years,
            "grades": self._safe_search_read('school360_academic.grade', domain, ['id', 'name']),
            "sections": self._safe_search_read('school360_academic.section', domain, ['id', 'name', 'grade_id']),
            "student_types": [
                {'id': 'active', 'name': 'Active'},
                {'id': 'transferred', 'name': 'Transferred'},
                {'id': 'graduated', 'name': 'Graduated'},
                {'id': 'dropped', 'name': 'Dropped'}
            ]
        }

    @api.model
    @tools.ormcache('self.env.uid', 'self.env.company.id', 'tuple(filters.items()) if filters else None')
    def get_all_stats(self, filters=None):
        """
        Fetches all dashboard statistics. 
        Uses safe search methods to prevent KeyError if sub-modules are missing.
        """
        company = self.env.company
        user = self.env.user
        filters = filters or {}
        currency_symbol = company.currency_id.symbol or '$'
        base_domain = [('company_id', '=', company.id)]
        student_domain = list(base_domain)
        attendance_domain = [('session_id.company_id', '=', company.id)]

        if filters.get('year_id'):
            y_id = int(filters['year_id'])
            student_domain.append(('academic_year_id', '=', y_id))
            attendance_domain.append(('session_id.academic_year_id', '=', y_id))
        if filters.get('grade_id'):
            g_id = int(filters['grade_id'])
            student_domain.append(('grade_id', '=', g_id))
            attendance_domain.append(('session_id.grade_id', '=', g_id))
        if filters.get('section_id'):
            s_id = int(filters['section_id'])
            student_domain.append(('section_id', '=', s_id))
            attendance_domain.append(('session_id.section_id', '=', s_id))
        if filters.get('student_type'):
            student_domain.append(('status', '=', filters['student_type']))

        employee = self.env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
        user_image = employee.image_128 if employee and employee.image_128 else user.image_128

        def get_count(model, domain):
            return self.env[model].search_count(domain) if model in self.env.registry else 0

        def get_group_data(model, group_field, domain):
            if model not in self.env.registry:
                return {"labels": [], "data": []}
            try:
                groups = self.env[model].read_group(domain, [group_field], [group_field])
                return {
                    "labels": [str(g[group_field][1] if isinstance(g[group_field], tuple) else g[group_field]).capitalize() for g in groups if g[group_field]],
                    "data": [g[group_field + '_count'] for g in groups if g[group_field]]
                }
            except Exception:
                return {"labels": [], "data": []}

        # Financials
        total_paid = 0
        total_due = 0
        total_revenue = 0
        collection_rate = 0
        pay_method_chart = {"labels": [], "data": []}

        if 'school360.fees' in self.env.registry:
            fee_domain = list(base_domain)
            if filters.get('grade_id'):
                fee_domain.append(('structure_id.grade_id', '=', int(filters['grade_id'])))
            
            fees = self.env['school360.fees'].search(fee_domain)
            total_revenue = sum(fees.mapped('total_amount'))
            total_paid = sum(fees.mapped('amount_paid'))
            total_due = sum(fees.mapped('amount_due'))
            collection_rate = round((total_paid / total_revenue * 100), 1) if total_revenue > 0 else 0

            if 'school360.fees.payment' in self.env.registry:
                pay_domain = [('fee_id', 'in', fees.ids)]
                pay_groups = self.env['school360.fees.payment'].read_group(pay_domain, ['payment_method', 'amount'], ['payment_method'])
                selection_dict = dict(self.env['school360.fees.payment']._fields['payment_method'].selection)
                pay_method_chart = {
                    "labels": [selection_dict.get(g['payment_method'], 'Other') for g in pay_groups if g['payment_method']],
                    "data": [g['amount'] for g in pay_groups if g['payment_method']]
                }

        # Attendance
        att_ratio = 0
        present_att = 0
        absent_att = 0
        if 'attendance.line' in self.env.registry:
            total_att = self.env['attendance.line'].search_count(attendance_domain)
            present_att = self.env['attendance.line'].search_count(attendance_domain + [('status', '=', 'present')])
            absent_att = self.env['attendance.line'].search_count(attendance_domain + [('status', '=', 'absent')])
            att_ratio = round((present_att / total_att * 100), 1) if total_att > 0 else 0

        return {
            "user": {"name": user.name, "email": user.login, "image": user_image},
            "school_name": company.name,
            "overview": {
                "students": get_count('school360.student', student_domain),
                "staff": get_count('hr.employee', base_domain),
                "attendance_rate": att_ratio,
                "earnings": f"${total_paid:,.0f}",
                "earnings_series": {"labels": ['Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb'], "data": [200, 450, 300, 628, 400, 500]},
                "calendar_events": [] 
            },
            "students": {
                "total": get_count('school360.student', student_domain),
                "active": get_count('school360.student', student_domain + [('status', '=', 'active')]),
                "transferred": get_count('school360.student', student_domain + [('status', '=', 'transferred')]),
                "graduated": get_count('school360.student', student_domain + [('status', '=', 'graduated')]),
                "dropped": get_count('school360.student', student_domain + [('status', '=', 'dropped')]),
                "status_chart": get_group_data('school360.student', 'status', student_domain),
                "grade_chart": get_group_data('school360.student', 'grade_id', student_domain)
            },
            "attendance": {
                "present": present_att,
                "absent": absent_att,
                "status_chart": get_group_data('attendance.line', 'status', attendance_domain),
                "grade_bar": get_group_data('attendance.session', 'grade_id', base_domain),
                "period_pie": get_group_data('attendance.session', 'period_number', base_domain)
            },
            "academic": {
                "grades_count": get_count('school360_academic.grade', base_domain),
                "sections_count": get_count('school360_academic.section', base_domain),
                "grade_bar": get_group_data('school360_academic.section', 'grade_id', base_domain),
                "subject_pie": get_group_data('school360_academic.subject', 'grade_id', base_domain)
            },
            "staff": {
                "total": get_count('hr.employee', base_domain),
                "teachers": get_count('hr.employee', base_domain + [('job_id.name', 'ilike', 'Teacher')]),
                "dept_chart": get_group_data('hr.employee', 'department_id', base_domain),
                "job_pie": get_group_data('hr.employee', 'job_id', base_domain)
            },
            "library": {
                "total_books": get_count('library.book', base_domain),
                "borrows": get_count('library.borrow', base_domain + [('status', '=', 'borrowed')]),
                "overdue": get_count('library.borrow', base_domain + [('status', '=', 'overdue')]),
                "status_bar": get_group_data('library.borrow', 'status', base_domain),
                "cat_chart": get_group_data('library.book', 'category_id', base_domain)
            },
            "finance": {
                "total_revenue": f"{currency_symbol}{total_revenue:,.0f}",
                "paid": f"{currency_symbol}{total_paid:,.0f}",
                "due": f"{currency_symbol}{total_due:,.0f}",
                "collection_rate": collection_rate,
                "method_chart": pay_method_chart,
                "status_pie": {"labels": ["Collected", "Outstanding"], "data": [total_paid, total_due]}
            },
            "admission": {
                "total": get_count('student.admission', base_domain),
                "growth_bar": get_group_data('student.admission', 'application_date:month', base_domain), 
                "status_pie": get_group_data('student.admission', 'status', base_domain)
            }
        }