# -*- coding: utf-8 -*-
from odoo import http

# class DePayrollEnhance(http.Controller):
#     @http.route('/de_payroll_enhance/de_payroll_enhance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_payroll_enhance/de_payroll_enhance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_payroll_enhance.listing', {
#             'root': '/de_payroll_enhance/de_payroll_enhance',
#             'objects': http.request.env['de_payroll_enhance.de_payroll_enhance'].search([]),
#         })

#     @http.route('/de_payroll_enhance/de_payroll_enhance/objects/<model("de_payroll_enhance.de_payroll_enhance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_payroll_enhance.object', {
#             'object': obj
#         })