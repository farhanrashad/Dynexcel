# -*- coding: utf-8 -*-
import time
from datetime import datetime
from datetime import time as datetime_time
from dateutil import relativedelta

import babel

from odoo import api, fields, models, tools, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
     
    @api.onchange('employee_id', 'date_from', 'date_to')
    def onchange_employee(self):
        res = super(HrPayslip, self).onchange_employee()
        lst = []
        if self.date_from and self.date_to and self.contract_id:
            self._cr.execute("select count(id), sum(unit_amount) from account_analytic_line where date::date>='%s' and date::date<='%s' and employee_id=%d" % (self.date_from, self.date_to, self.employee_id.id))
            result = self._cr.fetchone()
            if result and result[0]:
                lst.append({'name': '%s Timesheets' % (self.employee_id.name),
                            'number_of_days': result[0],
                            'number_of_hours': result[1],
                            'code' : 'WORK200',
                            'contract_id': self.contract_id.id})
            # leave
            self._cr.execute("""select sum(number_of_days_temp)
                                from hr_holidays
                                where date_from::date >= '%s'
                                and date_to::date <= '%s'
                                and state = 'validate'
                                and type = 'remove'
                                and employee_id='%s'""" % (self.date_from, self.date_to, self.employee_id.id))
            result = self._cr.fetchone()
            if result:
                lst.append({'name': '%s Leave' % (self.employee_id.name),
                            'number_of_days': result[0] if result[0] else 0.00,
                            'code' : 'Leave',
                            'contract_id': self.contract_id.id})
        #self.worked_days_line_ids = False
        worked_days_lines = self.worked_days_line_ids.browse([])
        for r in lst:
            worked_days_lines += worked_days_lines.new(r)
        self.worked_days_line_ids += worked_days_lines
        return res
