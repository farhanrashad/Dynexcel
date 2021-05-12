# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrEmployeeNotice(models.Model):
    _name = 'hr.employee.notice'
    _rec_name = 'name'
    _description = 'Hr Employee Offence'

    name = fields.Char("Name", required=True)
    employee_id = fields.Many2one('hr.employee', 'Employee')
    parent_id = fields.Many2one('hr.employee', 'Manager')
    department_id = fields.Many2one('hr.employee', 'Department')
    user_id = fields.Many2one('res.user', 'User')
    job_title = fields.Char("Job Title", required=False)
    identity = fields.Char("Identification No", required=False)
    office_type = fields.Char("Office Type", required=False)
    warning_type = fields.Char("Warning Type", required=False)
    date = fields.Date(string='Creation Date', required=False)
    created_id = fields.Many2one('hr.employee', 'Created By')
    decision = fields.Text(string='Decision Of Interaction')
    improvement = fields.Text(string='Action Improvement')
    consequence = fields.Text(string='Consequence Future Interaction')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done', 'Done')
    ], readonly=True, index=True, copy=False, default='draft')





