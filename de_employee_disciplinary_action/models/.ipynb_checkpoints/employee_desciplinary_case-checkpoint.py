# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

READONLY_STATES = {
    'confirm': [('readonly', True)],
    'apply': [('readonly', True)],
    'done': [('readonly', True)],
    'cancel': [('readonly', True)],
}

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
            'state': 'apply',
        })

    state = fields.Selection([
        ('draft', 'Draft'),
        ('wait-resp', 'Waiting Response'),
        ('apply', 'Penalty Applied'),
        ('close', 'Close'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    name = fields.Char(string='Order Reference', readonly=True, copy=False,  index=True, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string='Employee', store=True)
    date = fields.Date(string='Date', required=True,store=True)
    case_type = fields.Many2one('hr.employee.disciplinary.action.type',required=True,string='Case Type',store=True)
    user_id = fields.Many2one('res.users', string='Issuer', store=True, required=True)
    note = fields.Html(string="Description" )

    apply_penalty = fields.Boolean(string='Apply Penalty')
    penalty_amount = fields.Monetary(string='Penalty Amount', )
    deduction_amount = fields.Monetary(string='Deduction', readonly=True, compute="_compute_all_amount")
    residual_amount = fields.Monetary(string='Residual', readonly=True, compute="_compute_all_amount")
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, states=READONLY_STATES,
                                  default=lambda self: self.env.user.company_id.currency_id)
    company_id = fields.Many2one('res.company', string='Company', required=True, states=READONLY_STATES, default=lambda self: self.env.user.company_id)
    attachment_ids = fields.Many2many('ir.attachment', 'disp_case_ir_attachments_rel',
                                      'case_id', 'attachment_id', string="Attachments",
                                      help="Attach")
    @api.model
    def create(self,values):
        seq = self.env['ir.sequence'].get('hr.employee.disciplinary.action') 
        values['name'] = seq
        res = super(EmployeeDesciplinaryCase,self).create(values)
        return res
    
    @api.multi
    def _compute_all_amount(self):
        amount = deduction = 0
        payslips = self.env['hr.payslip']
        input_rules = self.env['hr.payslip.input']

        for adv in self:
            amount = deduction = 0
            payslips = self.env['hr.payslip'].search([('employee_id','=',adv.employee_id.id),('date_from','<=',adv.date),('date_to','>=', adv.date)])
            for payslip in payslips:
                input_rules = self.env['hr.payslip.input'].search([('payslip_id', '=', payslip.id), ('code', '=', 'EPR')])
                for input in input_rules:
                    deduction += input.amount
            adv.update({
                'deduction_amount': deduction,
                'residual_amount': adv.penalty_amount - deduction,
            })


    