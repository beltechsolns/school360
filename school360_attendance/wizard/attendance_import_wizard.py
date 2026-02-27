from odoo import models, fields, api
from odoo.exceptions import UserError
import base64
import io
import csv
import xlrd  # for XLS/XLSX support

class AttendanceImportWizard(models.TransientModel):
    _name = "attendance.import.wizard"
    _description = "Attendance Import Wizard"

    file = fields.Binary("File", required=True)
    file_name = fields.Char("File Name")
    file_type = fields.Selection([('csv','CSV'), ('xlsx','XLSX')], string="File Type", required=True)

    def action_import(self):
        self.ensure_one()
        if self.file_type == 'csv':
            self._import_csv()
        else:
            self._import_xlsx()

    def _import_csv(self):
        try:
            data = base64.b64decode(self.file)
            f = io.StringIO(data.decode('utf-8'))
            reader = csv.DictReader(f)
            self._process_rows(reader)
        except Exception as e:
            raise UserError(f"CSV import failed: {e}")

    def _import_xlsx(self):
        try:
            data = base64.b64decode(self.file)
            workbook = xlrd.open_workbook(file_contents=data)
            sheet = workbook.sheet_by_index(0)
            headers = sheet.row_values(0)
            rows = [dict(zip(headers, sheet.row_values(r))) for r in range(1, sheet.nrows)]
            self._process_rows(rows)
        except Exception as e:
            raise UserError(f"XLSX import failed: {e}")

    def _process_rows(self, rows):
        success = 0
        fail = 0
        errors = []
        AttendanceSession = self.env['attendance.session']
        AttendanceLine = self.env['attendance.line']
        Student = self.env['school360_students.student']
        AcademicYear = self.env['school360_academic.academic_year']
        Grade = self.env['school360_academic.grade']
        Section = self.env['school360_academic.section']

        for row in rows:
            try:
                # Validate mandatory fields
                date = row.get('Date')
                academic_year = AcademicYear.search([('name','=',row.get('Academic Year'))], limit=1)
                grade = Grade.search([('name','=',row.get('Grade'))], limit=1)
                section = Section.search([('name','=',row.get('Section'))], limit=1)
                student = Student.search([('student_id','=',row.get('Student ID'))], limit=1)
                status = row.get('Status', '').lower()
                period_number = int(row.get('Period',1))

                if not all([date, academic_year, grade, section, student]):
                    raise UserError("Missing mandatory fields or invalid references.")

                # Get or create session
                session = AttendanceSession.search([
                    ('date','=',date),
                    ('academic_year_id','=',academic_year.id),
                    ('grade_id','=',grade.id),
                    ('section_id','=',section.id),
                    ('period_number','=',period_number)
                ], limit=1)
                if not session:
                    session = AttendanceSession.create({
                        'date': date,
                        'academic_year_id': academic_year.id,
                        'grade_id': grade.id,
                        'section_id': section.id,
                        'teacher_id': self.env.user.id,
                        'period_number': period_number,
                        'company_id': self.env.company.id,
                    })

                # Avoid duplicates
                line = AttendanceLine.search([('session_id','=',session.id), ('student_id','=',student.id)], limit=1)
                if not line:
                    AttendanceLine.create({
                        'session_id': session.id,
                        'student_id': student.id,
                        'status': status,
                    })
                success += 1

            except Exception as e:
                fail += 1
                errors.append(f"Row {row}: {str(e)}")

        # Display summary
        message = f"Import finished: {success} successful, {fail} failed."
        if errors:
            message += "\nErrors:\n" + "\n".join(errors)
        return self.env['ir.actions.client'].info({
            'title': 'Attendance Import',
            'message': message,
            'type': 'ir.actions.client',
        })