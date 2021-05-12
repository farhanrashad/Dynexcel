# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class EmployeeDesciplinaryCaseType(models.Model):
    _name = 'hr.employee.disciplinary.action.type'
    _description = 'HR Employee Desciplinary Case type'
    _order = 'name desc'


    name = fields.Char(string='Name', store=True, required=True)
    

    
class EmployeeDesciplinaryCase(models.Model):
    _name = 'hr.employee.disciplinary.action'
    _description = 'HR Employee Desciplinary Case'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = 'name desc'
    
    def action_case_send(self):
        template_id = self.env.ref('de_employee_disciplinary_action.email_template_edi_disciplinary_case').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
        self.write({
            'state': 'wait-resp',
        })    
        
    def action_waiting_case(self):
        self.write({
            'state': 'wait-resp',
        })    
       
    def action_close_case(self):
        self.write({
            'state': 'close',
        })
    
    def action_apply_penalty(self):
        self.write({
            'state': 'close',
        })

    state = fields.Selection([
        ('draft', 'Draft'),
        ('wait-resp', 'Waiting Response'),
        ('close', 'Close'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    name = fields.Char(string='Order Reference', readonly=True, copy=False,  index=True, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string='Employee', store=True)
    date = fields.Date(string='Date', required=True,store=True)
    case_type = fields.Many2one('hr.employee.disciplinary.action.type',required=True,string='Case Type',store=True)
    user_id = fields.Many2one('res.users', string='Issuer', store=True, required=True)
    note = fields.Html(string="Description" )

    apply_penalty = fields.Boolean(string='Apply Ppenalty')
    penalty_amount = fields.Float(string='Penalty Amount')
    attachment_ids = fields.Many2many('ir.attachment', 'disp_case_ir_attachments_rel',
                                      'case_id', 'attachment_id', string="Attachments",
                                      help="Attach")
    @api.model
    def create(self,values):
        seq = self.env['ir.sequence'].get('hr.employee.disciplinary.action') 
        values['name'] = seq
        res = super(EmployeeDesciplinaryCase,self).create(values)
        return res


    