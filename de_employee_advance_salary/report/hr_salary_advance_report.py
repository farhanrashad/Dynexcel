# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class HRSalaryAdvanceReport(models.Model):
    _name = "hr.salary.advance.report"
    _description = "Salary Advance Report"
    _auto = False
    _rec_name = 'name'
    _order = 'name'
    
    name = fields.Char('Reference', readonly=True)
    nbr_lines = fields.Integer('# of Lines', readonly=True)

    employee_id = fields.Many2one('hr.employee', 'Employee', readonly=True)
    
    adv = fields.Float('Advanced', readonly=True)
    ded = fields.Float('Deduction', readonly=True)
    balance = fields.Float('Balance', readonly=True, compute='_compute_balance')
    mon = fields.Char(string='Month')
    
    @api.depends('adv','ded')
    def _compute_balance(self):
        for line in self:
            line.balance = line.adv - line.ded
    
    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        with_ = ("WITH %s" % with_clause) if with_clause else ""

        select_ = """
        count(x.*) as nbr, min(x.employee_id) as id, x.employee_id, x.mon, sum(x.adv) as adv, sum(x.ded) as ded from (
         select p.employee_id, 0 as adv, i.amount as ded, to_char(p.date_from,'Mon-YYYY') as mon from hr_payslip_input i
join hr_payslip p on i.payslip_id = p.id
where i.code = 'SAR'
union all
select a.employee_id, a.amount as adv, 0 as ded, to_char(a.date,'Mon-YYYY') as mon
from hr_salary_advance a 
) x
group by x.mon, x.employee_id
"""

        for field in fields.values():
            select_ += field
        
        from_ = groupby_ = ''

        return '%s (SELECT %s %s %s)' % (with_, select_, from_, groupby_)

    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))