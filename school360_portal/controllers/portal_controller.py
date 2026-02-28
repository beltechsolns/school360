# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class StudentPortal(CustomerPortal):
    """Portal controller for student listing and dashboard."""

    @http.route(['/my/students'], type='http', auth="user", website=True)
    def portal_my_students(self, **kwargs):
        partner = request.env.user.partner_id
        # Only fetch students linked via guardians and still existing
        students = request.env['student.student'].sudo().search([
            ('guardian_ids', 'in', partner.id),
        ])
        values = {
            'students': students,
            'page_name': 'my_students',
        }
        return request.render('school360_portal.portal_my_students', values)


class SchoolPortal(http.Controller):
    """Portal routes for student profiles, attendance, library, and admission."""

    @http.route('/portal/dashboard', auth='user', website=True)
    def portal_dashboard(self, **kwargs):
        partner = request.env.user.partner_id
        students = request.env['student.student'].sudo().search([
            # ('guardian_ids', 'in', partner.id),
        ])
        return request.render('school360_portal.portal_dashboard', {'students': students})

    @http.route('/portal/student/<int:student_id>/profile', auth='user', website=True)
    def student_profile(self, student_id, **kwargs):
        student = request.env['student.student'].sudo().browse(student_id)
        if not student.exists():
            return request.not_found()
        return request.render('school360_portal.portal_student_profile', {'student': student})

    @http.route('/portal/student/<int:student_id>/attendance', auth='user', website=True)
    def student_attendance(self, student_id, **kwargs):
        student = request.env['student.student'].sudo().browse(student_id)
        if not student.exists():
            return request.not_found()
        attendance = request.env['attendance.line'].sudo().search([
            ('student_id', '=', student.id)
        ])
        return request.render('school360_portal.portal_student_attendance', {
            'student': student,
            'attendance': attendance
        })

    # Student Fees
    @http.route('/portal/student/<int:student_id>/fees', auth='user', website=True)
    def student_fees(self, student_id, **kwargs):
        student = request.env['student.student'].sudo().browse(student_id)
        if not student.exists():
            return request.not_found()
        fees = request.env['school360.fees'].sudo().search([('student_id', '=', student.id)])
        return request.render('school360_portal.portal_student_fees', {
            'student': student,
            'fees': fees
        })

    @http.route('/portal/student/<int:student_id>/library', auth='user', website=True)
    def student_library(self, student_id, **kwargs):
        student = request.env['student.student'].sudo().browse(student_id)
        if not student.exists():
            return request.not_found()
        loans = request.env['library.borrow'].sudo().search([
            ('borrower_student_id', '=', student.id)
        ])
        return request.render('school360_portal.portal_student_library', {
            'student': student,
            'loans': loans
        })

    @http.route('/portal/student/<int:student_id>/admission', auth='user', website=True)
    def student_admission(self, student_id, **kwargs):
        student = request.env['student.student'].sudo().browse(student_id)
        if not student.exists():
            return request.not_found()
        # Fetch latest admission record
        application = request.env['student.admission'].sudo().search([
            ('student_id', '=', student.id)
        ], limit=1)
        return request.render('school360_portal.portal_student_admission', {
            'student': student,
            'application': application,
        })