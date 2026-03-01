/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, onWillStart, useState, useEffect } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/assets";

export class School360Dashboard extends Component {
    static template = "school360_dashboard.DashboardMain";

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        
        this.state = useState({
            activeTab: 'base',
            isLoading: true,
            filters: {
                year_id: "",
                grade_id: "",
                section_id: "",
                student_type: ""
            },
            filterOptions: {
                years: [],
                grades: [],
                sections: [],
                student_types: []
            },
            data: {
                user: {},
                overview: { earnings_series: { data: [] } },
                students: { grade_chart: { data: [] }, status_chart: { data: [] } },
                academic: { grade_bar: { data: [] }, subject_pie: { data: [] } },
                admission: { growth_bar: { data: [] }, status_pie: { data: [] } },
                attendance: { grade_bar: { data: [] }, period_pie: { data: [] } },
                staff: { dept_chart: { data: [] }, job_pie: { data: [] } },
                library: { status_bar: { data: [] }, cat_chart: { data: [] } },
                finance: { chart: { data: [] } }
            }
        });
        
        this.chartInstances = [];

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
            // Load Filter Dropdowns
            const options = await this.orm.call("school360.dashboard", "get_filter_options", []);
            this.state.filterOptions = options;
            // Load Initial Stats
            await this.loadStats();
        });

        useEffect(() => {
            if (!this.state.isLoading) {
                this.renderCharts();
            }
            return () => this.destroyCharts();
        }, () => [this.state.activeTab, this.state.data, this.state.isLoading]);
    }

    async loadStats() {
        this.state.isLoading = true;
        const res = await this.orm.call("school360.dashboard", "get_all_stats", [], {
            filters: this.state.filters
        });
        if (res) {
            this.state.data = res;
        }
        this.state.isLoading = false;
    }

    async onFilterChange(key, ev) {
        this.state.filters[key] = ev.target.value;
        await this.loadStats();
    }

    setTab(tab) {
        this.state.activeTab = tab;
    }

    destroyCharts() {
        this.chartInstances.forEach(c => c.destroy());
        this.chartInstances = [];
    }

    renderCharts() {
        this.destroyCharts();
        const d = this.state.data;
        if (!d || this.state.isLoading) return;

        if (this.state.activeTab === 'base') {
            this.initChart('homeLine', 'line', d.overview.earnings_series, '#4e73df', 'Earnings');
            this.initChart('homePie', 'pie', d.students.status_chart, null, 'Student Mix');
            this.initChart('homeBar', 'bar', d.staff.dept_chart, '#1cc88a', 'Staff by Dept');
        } else if (this.state.activeTab === 'students') {
            this.initChart('studentBarChart', 'bar', d.students.grade_chart, '#4e73df', 'Students');
            this.initChart('studentPieChart', 'doughnut', d.students.status_chart, null, 'Status');
        } else if (this.state.activeTab === 'academic') {
            this.initChart('academicBar', 'bar', d.academic.grade_bar, '#36b9cc', 'Sections');
            this.initChart('academicPie', 'pie', d.academic.subject_pie, null, 'Subjects');
        } else if (this.state.activeTab === 'admission') {
            this.initChart('admissionBar', 'bar', d.admission.growth_bar, '#f6c23e', 'Growth');
            this.initChart('admissionPie', 'pie', d.admission.status_pie, null, 'Status');
        } else if (this.state.activeTab === 'attendance') {
            this.initChart('attBar', 'bar', d.attendance.grade_bar, '#1cc88a', 'Attendance');
            this.initChart('attPie', 'pie', d.attendance.period_pie, null, 'Periods');
        } else if (this.state.activeTab === 'staff') {
            this.initChart('staffBarChart', 'bar', d.staff.dept_chart, '#4e73df', 'Departments');
            this.initChart('staffPie', 'doughnut', d.staff.job_pie, null, 'Jobs');
        } else if (this.state.activeTab === 'library') {
            this.initChart('libraryPieChart', 'doughnut', d.library.cat_chart);
            this.initChart('libraryBarChart', 'bar', d.library.status_bar, '#36b9cc', 'Books');
        }
    }

    initChart(id, type, chartData, color = null, labelName = 'Data') {
        const el = document.getElementById(id);
        if (el && chartData && chartData.data && Array.isArray(chartData.data) && chartData.data.length > 0) {
            const config = {
                type: type,
                data: {
                    labels: chartData.labels,
                    datasets: [{
                        label: labelName,
                        data: chartData.data,
                        backgroundColor: color ? color : ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b'],
                        fill: type === 'line',
                        tension: 0.4
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false }
            };
            this.chartInstances.push(new Chart(el, config));
        }
    }
}
registry.category("actions").add("school360_dashboard_main", School360Dashboard);