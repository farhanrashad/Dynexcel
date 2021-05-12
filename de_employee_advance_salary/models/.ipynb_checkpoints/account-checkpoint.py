# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    hr_salary_advance_id = fields.Many2one('hr.salary.advance', string='Salary Advance')

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    hr_salary_advance_id = fields.Many2one('hr.salary.advance', string='Salary Advance')

