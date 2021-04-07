# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    location = fields.Char(string="Site Location")
    total_amount = fields.Float(string="Total Amount", compute='get_total' )
    desc_ids = fields.One2many('sale.order.description', 'sale_order_id', string="Description")
    
    def get_total(self):
        total = 0.0
        for rec in self.desc_ids:
            total = total + rec.amount
        self.total_amount = total
        
class SaleOrderDescription(models.Model):
    _name = 'sale.order.description'
    description = 'sale order description'
    
    name = fields.Text(string="Description")
    amount = fields.Float(string="Amount")
    sale_order_id = fields.Many2one('sale.order')
