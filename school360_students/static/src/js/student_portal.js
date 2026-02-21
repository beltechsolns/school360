/** @odoo-module **/
/**
 * School360 Students Portal JavaScript
 *
 * Provides interactive student card and enrollment table
 * functionality for the parent/guardian portal.
 */

import publicWidget from '@web/legacy/js/public/public_widget';

const StudentPortal = publicWidget.Widget.extend({
    selector: '.o_portal_student_details',

    start() {
        this._super(...arguments);
        this._initStudentCards();
        this._initEnrollmentTable();
    },

    _initStudentCards() {
        this.el.querySelectorAll('.student-card').forEach((card) => {
            card.addEventListener('click', (e) => {
                if (!e.target.closest('a, button')) {
                    const studentId = card.dataset.studentId;
                    if (studentId) {
                        window.location.href = `/my/student/${studentId}`;
                    }
                }
            });
        });
    },
    _forStudentCards(callback) {
        this.el.querySelectorAll('.student-card').forEach(callback);
    },

    _initEnrollmentTable() {
        this.el.querySelectorAll('.enrollment-table th.sortable').forEach((th) => {
            th.addEventListener('click', () => {
                const table = th.closest('table');
                const tbody = table.querySelector('tbody');
                const rows = Array.from(tbody.querySelectorAll('tr'));
                const colIdx = Array.from(th.parentNode.children).indexOf(th);
                const asc = !th.classList.contains('sort-asc');

                table.querySelectorAll('th').forEach((h) =>
                    h.classList.remove('sort-asc', 'sort-desc')
                );
                th.classList.add(asc ? 'sort-asc' : 'sort-desc');

                rows.sort((a, b) => {
                    let aVal = a.children[colIdx]?.textContent.trim() || '';
                    let bVal = b.children[colIdx]?.textContent.trim() || '';
                    if (th.classList.contains('date-column')) {
                        aVal = new Date(aVal);
                        bVal = new Date(bVal);
                    }
                    return asc
                        ? (aVal > bVal ? 1 : aVal < bVal ? -1 : 0)
                        : (aVal < bVal ? 1 : aVal > bVal ? -1 : 0);
                });

                tbody.replaceChildren(...rows);
            });
        });
    },
});

publicWidget.registry.StudentPortal = StudentPortal;

export default StudentPortal;
