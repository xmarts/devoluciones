# -*- coding: utf-8 -*-
from odoo import http

# class ReturnProducts(http.Controller):
#     @http.route('/return_products/return_products/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/return_products/return_products/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('return_products.listing', {
#             'root': '/return_products/return_products',
#             'objects': http.request.env['return_products.return_products'].search([]),
#         })

#     @http.route('/return_products/return_products/objects/<model("return_products.return_products"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('return_products.object', {
#             'object': obj
#         })