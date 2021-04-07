# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    sale_id = fields.Many2one('sale.order',compute='get_ref' )

    def get_ref(self):
        rec = self.env['sale.order'].search([('name','=',self.invoice_origin)])
        self.sale_id = rec.id