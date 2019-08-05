# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime, time
from dateutil.relativedelta import relativedelta
from odoo import api, models, _
from odoo.exceptions import UserError


class ReportAttendanceTemplate(models.AbstractModel):
    _name = 'report.attendance_report.report_attendance_template'
    
    @api.model
    def get_report_values(self, docids, data=None):
        if not data.get('form'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        return {
            'data': data.get('form'),

        }


class AttendanceReport(models.TransientModel):
    _name = 'attendance.report'
    _description = "Attendance Report Wizard"

    from_date = fields.Date('From Date', default=lambda self: fields.Date.to_string(date.today().replace(day=1)),
                            required=True)
    to_date = fields.Date("To Date", default=lambda self: fields.Date.to_string(
        (datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()), required=True)
    employee_id = fields.Many2many('hr.employee', string="Employee")

    @api.multi
    def print_report(self):
        domain = []
        datas = []
        if self.employee_id:
            domain.append(('id', 'in', self.employee_id.ids))

        employees = self.env['hr.employee'].search(domain)
        for employee in employees:
            present = 0
            absent = 0
            date_from = datetime.combine(fields.Datetime.from_string(str(self.from_date)), time.min)
            date_to = datetime.combine(fields.Datetime.from_string(str(self.to_date)), time.max)
            intervals = employee.resource_calendar_id._iter_work_days(date_from, date_to, employee.resource_id.id)
            for rec in intervals:
                attendances = self.env["hr.attendance"].search(
                    [('employee_id', '=', employee.id), ('check_in', '>=', str(rec)),
                     ('check_in', '<=', str(rec))])
                if attendances:
                    present += 1
                else:
                    absent += 1
            datas.append({
                    'id': employee.id,
                    'name':employee.name,
                    'present': present,
                    'absent': absent,
                })
        res = {
            'attendances':datas,
            'start_date': self.from_date,
            'end_date': self.to_date,
        }
        data = {
            'form': res,
        }
        return self.env.ref('attendance_report.report_hr_attendance').report_action([],data=data)
