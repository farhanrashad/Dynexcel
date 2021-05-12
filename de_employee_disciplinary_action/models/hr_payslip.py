# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models,api


class HRPayslip(models.Model):
    _inherit = 'hr.payslip'
    def compute_sheet(self):
        for payslip in self:
            amount = 0 
            adv_salary = self.env['hr.employee.disciplinary.action'].search([('employee_id', '=', payslip.employee_id.id), ('apply_penalty', '=', True), ('state', 'in', ['close','done'])])
        
            if adv_salary:
                for adv_obj in adv_salary:
                    current_date = datetime.strptime(str(payslip.date_from), '%Y-%m-%d').date().month
                    adv_date = adv_obj.date
                    existing_date = datetime.strptime(str(adv_date), '%Y-%m-%d').date().month
                    if current_date == existing_date:
                        amount += adv_obj.penalty_amount
            
                        input_exists = self.env['hr.payslip.input'].search([('payslip_id', '=', payslip.id), ('code', '=', 'EPR')])
                                
                        if not input_exists:
                            input_type_exists = self.env['hr.contract.advantage.template'].search([('code', '=', 'EPR')])            
                            input_exists.create({
                              'input_type_id': input_type_exists.id,
                              'code': 'EPR',
                              'amount': amount,
                              'contract_id': payslip.contract_id.id,
                              'payslip_id': self.id,
                              })
                        else:
                            if not input_exists:
                                input_exists.write({
                                    'amount': amount,
                                })
        rec = super(HRPayslip, self).compute_sheet()
        return rec
            
    
    
    
    
    