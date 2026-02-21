/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, onMounted, useState, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class StudentDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");

        this.state = useState({
            totalStudents: 0,
            activeStudents: 0,
            totalEnrollments: 0,
            statusCounts: {
                draft: 0,
                active: 0,
                transferred: 0,
                graduated: 0,
                dropped: 0
            },
            gradeEnrollments: {}, 
        });

        this.pieChartRef = useRef("pieChart");
        this.barChartRef = useRef("barChart");

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
            await this.fetchDashboardData();
        });

        onMounted(() => {
            this.renderCharts();
        });
    }

    async fetchDashboardData() {
        const students = await this.orm.readGroup(
            "student.student",
            [],
            ["status"],
            ["status"]
        );

        let total = 0;
        let active = 0;

        students.forEach((group) => {
            const count = group.status_count;
            total += count;
            this.state.statusCounts[group.status] = count;
            if (group.status === 'active') {
                active = count;
            }
        });

        this.state.totalStudents = total;
        this.state.activeStudents = active;

        this.state.totalEnrollments = await this.orm.searchCount(
            "student.enrollment",
            []
        );

        const gradeData = await this.orm.readGroup(
            "student.enrollment",
            [],
            ["grade_id"],
            ["grade_id"]
        );

        gradeData.forEach((group) => {
            const grade = group.grade_id || 'Unassigned';
            this.state.gradeEnrollments[grade] = group.grade_id_count;
        });
    }

    renderCharts() {
        if (this.pieChartRef.el) {
            new Chart(this.pieChartRef.el, {
                type: 'pie',
                data: {
                    labels: ['Draft', 'Active', 'Graduated', 'Transferred', 'Dropped'],
                    datasets: [{
                        data: [
                            this.state.statusCounts.draft,
                            this.state.statusCounts.active,
                            this.state.statusCounts.graduated,
                            this.state.statusCounts.transferred,
                            this.state.statusCounts.dropped
                        ],
                        backgroundColor: ['#ffc107', '#198754', '#0d6efd', '#0dcaf0', '#dc3545'],
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false }
            });
        }

        if (this.barChartRef.el) {
            new Chart(this.barChartRef.el, {
                type: 'bar',
                data: {
                    labels: Object.keys(this.state.gradeEnrollments),
                    datasets: [{
                        label: 'Enrollments',
                        data: Object.values(this.state.gradeEnrollments),
                        backgroundColor: '#6f42c1',
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        yAxes: [{ ticks: { beginAtZero: true } }]
                    }
                }
            });
        }
    }

    openStudents(status = false) {
        let domain = [];
        if (status) {
            domain = [['status', '=', status]];
        }

        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Students",
            res_model: "student.student",
            views: [[false, "list"], [false, "form"]],
            domain: domain,
            target: "current",
        });
    }

    openEnrollments() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Enrollments",
            res_model: "student.enrollment",
            views: [[false, "list"], [false, "form"]],
            target: "current",
        });
    }
}

StudentDashboard.template = "school360_students.Dashboard";
StudentDashboard.components = {};

registry.category("actions").add("school360_students.dashboard", StudentDashboard);
