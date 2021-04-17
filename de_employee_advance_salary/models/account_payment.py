# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    hr_salary_advance_id = fields.Many2one('hr.salary.advance', string='Salary Advance')


    
class hetPayment(models.Model):
    _inherit = 'hr.employee'

    task_ids = fields.Many2one('project.task', string='Task')

