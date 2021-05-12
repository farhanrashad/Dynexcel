# -*- coding: utf-8 -*-
# from odoo import http


# class DeEmployeeDisciplinaryCase(http.Controller):
#     @http.route('/de_employee_disciplinary_case/de_employee_disciplinary_case/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_employee_disciplinary_case/de_employee_disciplinary_case/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_employee_disciplinary_case.listing', {
#             'root': '/de_employee_disciplinary_case/de_employee_disciplinary_case',
#             'objects': http.request.env['de_employee_disciplinary_case.de_employee_disciplinary_case'].search([]),
#         })

#     @http.route('/de_employee_disciplinary_case/de_employee_disciplinary_case/objects/<model("de_employee_disciplinary_case.de_employee_disciplinary_case"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_employee_disciplinary_case.object', {
#             'object': obj
#         })
