# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Users(models.Model):
    _inherit = 'res.users'

    menu_ids = fields.Many2many('ir.ui.menu', 'user_menu_rel', 'uid', 'menu_id', string='Menu To Hide', help='Select Menus To Hide From This User')


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        menus = super(IrUiMenu, self).search(args, offset=0, limit=None, order=order, count=False)
        user = self.env['res.users'].browse(self._uid)
        if menus:
            for menu in user.menu_ids:
                if menu in menus:
                    menus -= menu
            if offset:
                menus = menus[offset:]
            if limit:
                menus = menus[:limit]
        return len(menus) if count else menus
