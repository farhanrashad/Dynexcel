# -*- coding: utf-8 -*-
# from odoo import http


# class DeProjectInvoice(http.Controller):
#     @http.route('/de_project_invoice/de_project_invoice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_project_invoice/de_project_invoice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_project_invoice.listing', {
#             'root': '/de_project_invoice/de_project_invoice',
#             'objects': http.request.env['de_project_invoice.de_project_invoice'].search([]),
#         })

#     @http.route('/de_project_invoice/de_project_invoice/objects/<model("de_project_invoice.de_project_invoice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_project_invoice.object', {
#             'object': obj
#         })
