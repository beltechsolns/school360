# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class StudentPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        """Add student counters to portal home."""
        values = super()._prepare_home_portal_values(counters)

        if 'student_count' in counters:
            partner = request.env.user.partner_id
            students = request.env['student.student'].search([
                ('guardian_ids', 'in', [partner.id]),
            ])
            values['student_count'] = len(students)

        return values

    @http.route(
        ['/my/students', '/my/students/page/<int:page>'],
        type='http', auth='user', website=True,
    )
    def portal_my_students(self, page=1, sortby=None, search=None,
                           search_in='all', **kwargs):
        """Display students linked to the current user (parent/guardian)."""
        values = self._prepare_portal_layout_values()

        partner = request.env.user.partner_id
        Student = request.env['student.student']

        domain = [('guardian_ids', 'in', [partner.id])]

        # Search
        searchbar_inputs = {
            'all': {'input': 'all', 'label': _('Search in All'), 'domain': []},
            'name': {'input': 'name', 'label': _('Name'),
                     'domain': [('name', 'ilike', search)]},
            'student_id': {'input': 'student_id', 'label': _('Student ID'),
                           'domain': [('student_id', 'ilike', search)]},
        }

        search_domain = []
        if search and search_in:
            search_domain = searchbar_inputs.get(search_in, {}).get('domain', [])
        domain += search_domain

        # Sort
        searchbar_sortings = {
            'name': {'label': _('Name'), 'order': 'name asc'},
            'student_id': {'label': _('Student ID'), 'order': 'student_id asc'},
        }
        if not sortby:
            sortby = 'name'
        order = searchbar_sortings[sortby]['order']

        # Pager
        student_count = Student.search_count(domain)
        pager = portal_pager(
            url='/my/students',
            total=student_count,
            page=page,
            step=10,
            url_args={'sortby': sortby, 'search': search, 'search_in': search_in},
        )

        students = Student.search(
            domain, order=order, limit=10, offset=pager['offset'],
        )

        values.update({
            'students': students,
            'page_name': 'student',
            'pager': pager,
            'default_url': '/my/students',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_inputs': searchbar_inputs,
            'search': search,
            'search_in': search_in,
        })
        return request.render('school360_students.portal_my_students', values)

    @http.route(
        ['/my/student/<int:student_id>'],
        type='http', auth='user', website=True,
    )
    def portal_student_page(self, student_id, **kwargs):
        """Display detailed student information for parents/guardians."""
        values = self._prepare_portal_layout_values()

        partner = request.env.user.partner_id
        student = request.env['student.student'].browse(student_id)

        # Security: user must be a guardian of this student
        if not student.exists() or partner not in student.guardian_ids:
            return request.redirect('/my/students')

        enrollments = request.env['student.enrollment'].search([
            ('student_id', '=', student_id),
        ], order='enrollment_date desc')

        values.update({
            'student': student,
            'enrollments': enrollments,
            'page_name': 'student',
        })
        return request.render('school360_students.portal_student_page', values)

    @http.route(
        ['/my/student/<int:student_id>/enrollments'],
        type='http', auth='user', website=True,
    )
    def portal_student_enrollments(self, student_id, **kwargs):
        """Display student enrollment history."""
        values = self._prepare_portal_layout_values()

        partner = request.env.user.partner_id
        student = request.env['student.student'].browse(student_id)

        if not student.exists() or partner not in student.guardian_ids:
            return request.redirect('/my/students')

        enrollments = request.env['student.enrollment'].search([
            ('student_id', '=', student_id),
        ], order='enrollment_date desc')

        values.update({
            'student': student,
            'enrollments': enrollments,
            'page_name': 'student_enrollments',
        })
        return request.render('school360_students.portal_student_enrollments', values)
