# -*- coding: utf-8 -*-
# from odoo import http


# class School360(http.Controller):
#     @http.route('/school360/school360', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/school360/school360/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('school360.listing', {
#             'root': '/school360/school360',
#             'objects': http.request.env['school360.school360'].search([]),
#         })

#     @http.route('/school360/school360/objects/<model("school360.school360"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('school360.object', {
#             'object': obj
#         })

