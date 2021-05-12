# -*- coding: utf-8 -*-
from odoo import http

# class DePayrollTimesheet(http.Controller):
#     @http.route('/de_payroll_timesheet/de_payroll_timesheet/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_payroll_timesheet/de_payroll_timesheet/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_payroll_timesheet.listing', {
#             'root': '/de_payroll_timesheet/de_payroll_timesheet',
#             'objects': http.request.env['de_payroll_timesheet.de_payroll_timesheet'].search([]),
#         })

#     @http.route('/de_payroll_timesheet/de_payroll_timesheet/objects/<model("de_payroll_timesheet.de_payroll_timesheet"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_payroll_timesheet.object', {
#             'object': obj
#         })