# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrEmployeeOffence(models.Model):
    _name = 'hr.employee.offence'
    _rec_name = 'name'
    _description = 'Hr Employee Offence'

    name = fields.Char("Name", required=True)

