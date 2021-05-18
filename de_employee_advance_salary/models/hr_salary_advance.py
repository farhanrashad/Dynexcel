# -*- coding: utf-8 -*-
import time
from datetime import datetime
from odoo import fields, models, api, _
from odoo.exceptions import except_orm
from odoo import exceptions
from odoo.exceptions import UserError, ValidationError

READONLY_STATES = {
    'confirm': [('readonly', True)],
    'approval1': [('readonly', True)],
    'approval2': [('readonly', True)],
    'approval3': [('readonly', True)],
    'paid': [('readonly', True)],
    'done': [('readonly', True)],
    'cancel': [('readonly', True)],
}

PAYMENT_READONLY_STATES = {
    'paid': [('readonly', True)],
    'done': [('readonly', True)],
    'cancel': [('readonly', True)],
}


class HRSalaryAdvance(models.Model):
    _name = "hr.salary.advance"
    _description = 'Employee Advance Salary'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, states=READONLY_STATES,)
    department_id = fields.Many2one('hr.department', string='Department', related='employee_id.department_id', readonly=True)
    job_title = fields.Many2one(related='employee_id.job_id',readonly=True)
    employee_contract_id = fields.Many2one('hr.contract', string='Contract', required=True, states=READONLY_STATES, domain="[('employee_id','=',employee_id)]")
    date = fields.Date(string='Request Date', required=True, states=READONLY_STATES, default=lambda self: fields.Date.today())
    reason = fields.Text(string='Reason')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, states=READONLY_STATES,
                                  default=lambda self: self.env.user.company_id.currency_id)
    company_id = fields.Many2one('res.company', string='Company', required=True, states=READONLY_STATES, default=lambda self: self.env.user.company_id)
    user_id = fields.Many2one('res.users', string='Requester', states=READONLY_STATES, tracking=True, default=lambda self: self.env.user)

    amount = fields.Monetary(string='Request Amount', required=True, states=READONLY_STATES,)
    exceed_condition = fields.Boolean(string='Exceed than maximum', help="The Advance is greater than the maximum percentage in salary structure", states=READONLY_STATES,)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirmed'),
                              ('approval1', 'Approved by Manager'),
                              ('approval2', 'Approved by HR'),
                              ('approval3', 'Approved by Director'),
                              ('paid', 'Paid'),
                              ('cancel', 'Reject'),
                              ('done', 'Done'),], string='Status', default='draft', track_visibility='onchange')
    
    deductable = fields.Boolean(string='Deductable', default=True, states=PAYMENT_READONLY_STATES,)
    partner_id = fields.Many2one('res.partner', string='Partner', states=PAYMENT_READONLY_STATES)
    journal_id = fields.Many2one('account.journal', string='Journal', domain="[('type','in',['cash','bank','purchase'])]", states=PAYMENT_READONLY_STATES)
    journal_type = fields.Selection(related='journal_id.type', readonly=True)

    payment_id = fields.Many2one('account.payment', string='Payment', readonly=True, compute='_get_payment')
    paid_amount = fields.Monetary(string='Paid Amount', readonly=True, compute="_compute_all_amount")
    deduction_amount = fields.Monetary(string='Deduction', readonly=True, compute="_compute_all_amount")
    residual_amount = fields.Monetary(string='Residual', readonly=True, compute="_compute_all_amount")

    account_id = fields.Many2one('account.account',string="Account", states=PAYMENT_READONLY_STATES)
    payment_method_id = fields.Many2one('account.payment.method', string='Payment Method Type', oldname="payment_method", states=PAYMENT_READONLY_STATES)
    
    
        
    bill_count = fields.Integer(string='Vendor Bill', compute='get_bill_count')
    payment_count = fields.Integer(string='Payment', compute='get_payment_count')
    
    #@api.depends('order_line.price_total')
    @api.multi
    def _compute_all_amount(self):
        amount = deduction = 0
        invoices = self.env['account.invoice']
        payments = self.env['account.payment']
        payslips = self.env['hr.payslip']
        input_rules = self.env['hr.payslip.input']

        for adv in self:
            amount = deduction = 0
            invoices = self.env['account.invoice'].search([('hr_salary_advance_id', '=', adv.id)])
            payments = self.env['account.payment'].search([('hr_salary_advance_id', '=', adv.id)])
            payslips = self.env['hr.payslip'].search([('employee_id','=',adv.employee_id.id),('date_from','<=',adv.date),('date_to','>=', adv.date)])
            for payslip in payslips:
                input_rules = self.env['hr.payslip.input'].search([('payslip_id', '=', payslip.id), ('code', '=', 'SAR')])
                for input in input_rules:
                    deduction += input.amount
            if adv.journal_id.type == 'purchase':
                for invoice in invoices:
                    amount += invoice.amount_total
            else:
                for payment in payments:
                    amount += payment.amount
            adv.update({
                'paid_amount': amount,
                'deduction_amount': deduction,
                'residual_amount': amount - deduction,
            })
        
    def get_bill_count(self):
        count = self.env['account.invoice'].search_count([('hr_salary_advance_id', '=', self.id)])
        self.bill_count = count
        
    def get_payment_count(self):
        count = self.env['account.payment'].search_count([('hr_salary_advance_id', '=', self.id)])
        self.payment_count = count
    
    @api.depends('state')
    def _get_payment(self):
        payment_id = self.env['account.payment'].search([('hr_salary_advance_id','=',self.id)],limit=1)
        self.payment_id = payment_id.id
        if not payment_id:
            self.payment_id = False
            
    #@api.constrains('amount')
    #def _check_amount(self):
        #if self.amount:
            #contract_id = self.env['hr.contract'].search([('employee_id','=', self.employee_id.id),('state','=','open')], limit=1)       
            #self.employee_contract_id = contract_id.id
            #adv = self.amount
            #amt = (self.employee_contract_id.max_percent * self.employee_contract_id.wage) / 100
            #if adv > amt and not self.exceed_condition:
                #raise UserError(('Error!', 'Advance amount is greater than allotted. You are only allow to enter Amount '+str(amt)))

    def unlink(self):
        if any(self.filtered(lambda loan: loan.state not in ('draft', 'cancel'))):
            raise UserError(_('You cannot delete a Request which is not draft or cancelled!'))
        return super(HRSalaryAdvance, self).unlink()

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        if self.employee_id:
            contract_id = self.env['hr.contract'].search([('employee_id','=',self.employee_id.id),('state','=','open')])
            self.employee_contract_id = contract_id.id
            self.partner_id = self.employee_id.address_home_id.id
    
    @api.model
    def create(self, vals):
            
        vals['name'] = self.env['ir.sequence'].get('hr.salary.advance') or ' '
        if vals['amount']==0:
            raise UserError('You Should enter Required amount Greater Than 0. ')
        res_id = super(HRSalaryAdvance, self).create(vals)
        return res_id
    
   
    def action_confirm(self):
        self.state = 'confirm'

    def action_approval1(self):
        """This Approve the employee salary advance request.
                   """
        emp_obj = self.env['hr.employee']
        address = emp_obj.browse([self.employee_id.id]).address_home_id

        salary_advance_search = self.search([('employee_id', '=', self.employee_id.id), ('id', '!=', self.id),
                                             ('state', '=', 'approve')])
        current_month = datetime.strptime(str(self.date), '%Y-%m-%d').date().month
        for each_advance in salary_advance_search:
            existing_month = datetime.strptime(str(each_advance.date), '%Y-%m-%d').date().month
            if current_month == existing_month:
                raise UserError(('Error!', 'Advance can be requested once in a month'))
                
        salary_advance_search = self.search([('employee_id', '=', self.employee_id.id), ('id', '!=', self.id), ('id', '!=', self.id),
                                             ('state', '=', 'approve')])
        current_year = datetime.strptime(str(self.date), '%Y-%m-%d').date().year
        for each_advance in salary_advance_search:
            existing_year = datetime.strptime(str(each_advance.date), '%Y-%m-%d').date().year
        
        struct_id = self.employee_id.contract_id
        contract = self.env['hr.contract'].search([('state','=','open'),('employee_id','=',self.employee_id.id)])
        if(self.employee_contract_id.id == False):
            self.employee_contract_id = contract
        if not struct_id.max_percent or not struct_id.advance_date:
            raise UserError(('Error!', 'Max percentage or advance days are not provided in Contract'))
        adv = self.amount
        amt = (self.employee_contract_id.max_percent * self.employee_contract_id.wage) / 100
        if adv > amt and not self.exceed_condition:
            raise UserError(('Error!', 'Advance amount is greater than allotted'))

        if not self.amount:
            raise UserError(('Warning', 'You must Enter the Salary Advance amount'))
        payslip_obj = self.env['hr.payslip'].search([('employee_id', '=', self.employee_id.id),
                                                     ('state', '=', 'done'), ('date_from', '<=', self.date),
                                                     ('date_to', '>=', self.date)])
        if payslip_obj:
            raise UserError(('Warning', "This month salary already calculated"))

        for slip in self.env['hr.payslip'].search([('employee_id', '=', self.employee_id.id)]):
            slip_moth = datetime.strptime(str(slip.date_from), '%Y-%m-%d').date().month
            if current_month == slip_moth + 1:
                slip_day = datetime.strptime(str(slip.date_from), '%Y-%m-%d').date().day
                current_day = datetime.strptime(str(self.date), '%Y-%m-%d').date().day
                if current_day - slip_day < struct_id.advance_date:
                    raise exceptions.Warning(
                        _('Request can be done after "%s" Days From prevoius month salary') % struct_id.advance_date)
        self.state = 'approval1'

    def action_approval2(self):
        self.state = 'approval2'
        
    def action_approval3(self):
        """This Approve the employee salary advance request from accounting department.
                   """
        emp_obj = self.env['hr.employee']
        address = emp_obj.browse([self.employee_id.id]).address_home_id

        salary_advance_search = self.search([('employee_id', '=', self.employee_id.id), ('id', '!=', self.id),
                                             ('state', '=', 'approve')])
        current_month = datetime.strptime(str(self.date), '%Y-%m-%d').date().month
        for each_advance in salary_advance_search:
            existing_month = datetime.strptime(str(each_advance.date), '%Y-%m-%d').date().month
            if current_month == existing_month:
                raise UserError(('Error!', 'Advance can be requested once in a month'))
                
        salary_advance_search = self.search([('employee_id', '=', self.employee_id.id), ('id', '!=', self.id), ('id', '!=', self.id),
                                             ('state', '=', 'approve')])
        current_year = datetime.strptime(str(self.date), '%Y-%m-%d').date().year
        for each_advance in salary_advance_search:
            existing_year = datetime.strptime(str(each_advance.date), '%Y-%m-%d').date().year

           
        struct_id = self.employee_id.contract_id
        contract = self.env['hr.contract'].search([('state','=','open'),('employee_id','=',self.employee_id.id)])
        if(self.employee_contract_id.id == False):
            self.employee_contract_id = contract
        if not struct_id.max_percent or not struct_id.advance_date:
            raise UserError(('Error!', 'Max percentage or advance days are not provided in Contract'))
        adv = self.amount
        amt = (self.employee_contract_id.max_percent * self.employee_contract_id.wage) / 100
        if adv > amt and not self.exceed_condition:
            raise UserError(('Error!', 'Advance amount is greater than allotted'))

        if not self.amount:
            raise UserError(('Warning', 'You must Enter the Salary Advance amount'))
        payslip_obj = self.env['hr.payslip'].search([('employee_id', '=', self.employee_id.id),
                                                     ('state', '=', 'done'), ('date_from', '<=', self.date),
                                                     ('date_to', '>=', self.date)])
        if payslip_obj:
            raise UserError(('Warning', "This month salary already calculated"))

        for slip in self.env['hr.payslip'].search([('employee_id', '=', self.employee_id.id)]):
            slip_moth = datetime.strptime(str(slip.date_from), '%Y-%m-%d').date().month
            if current_month == slip_moth + 1:
                slip_day = datetime.strptime(str(slip.date_from), '%Y-%m-%d').date().day
                current_day = datetime.strptime(str(self.date), '%Y-%m-%d').date().day
                if current_day - slip_day < struct_id.advance_date:
                    raise exceptions.Warning(
                        _('Request can be done after "%s" Days From prevoius month salary') % struct_id.advance_date)
        if not self.amount:
            raise UserError(('Warning', 'You must Enter the Salary Advance amount'))


        self.state = 'approval3'
        return True
    
    def action_view_invoice(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'binding_type': 'action',
            'name': 'Vendor Bill',
            'domain': [('hr_salary_advance_id','=', self.id)],
            'target': 'current',
            'res_model': 'account.invoice',
            'view_mode': 'tree,form',
        }
    def action_view_payment(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'binding_type': 'action',
            'name': 'Payment',
            'domain': [('hr_salary_advance_id','=', self.id)],
            'target': 'current',
            'res_model': 'account.payment',
            'view_mode': 'tree,form',
        }

    def action_cancel(self):
        self.state = 'cancel'

    def action_done(self):
        self.state = 'done'

    def action_payment(self):
        invoice = False
        if self.journal_id.type == 'purchase':
            invoice = self.env['account.invoice']
            lines_data = []
            lines_data.append([0,0,{
                'name': self.name,
                'price_unit': self.amount,
                'account_id': self.account_id.id,
                'quantity': 1,
            }])
            invoice.create({
                'partner_id': self.partner_id.id,
                'type': 'in_invoice',
                'reference': self.name,
                'origin': self.name,
                'date_invoice':self.date,
                'journal_id':self.journal_id.id,
                'hr_salary_advance_id':self.id,
                'invoice_line_ids':lines_data,
            })
        
        elif self.journal_id.type in ('bank','cash'):
            payment = self.env['account.payment']
            payment.create({
                'payment_type': 'outbound',
                'partner_type': 'supplier',
                'partner_id': self.partner_id.id,
                'payment_method_id': self.payment_method_id.id,
                'company_id': self.company_id.id,
                'amount': self.amount,
                'currency_id': self.currency_id.id,
                'journal_id': self.journal_id.id,
                'date': fields.Date.today(),
                'ref': self.name,
                'hr_salary_advance_id':self.id,
            })
        self.update({
            'state': 'paid'
        })
        return invoice
    
        