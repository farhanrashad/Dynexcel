# -*- coding: utf-8 -*-

{
    'name': 'HRMS Advance Salary',
    'version': '14.0.0.3',
    'summary': 'Advance Salary In HR',
    'description': """
        Helps you to manage Advance Salary Request of your company's staff.
        """,
    'category': 'Human/Resources',
    'author': "Dynexcel",
    'company': 'Dynexcel',
    'maintainer': 'Dynexcel',
    'website': "https://www.dynexcel.com",
    'depends': [
        'hr_payroll', 'base' , 'hr', 'account_accountant', 'hr_contract',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/salary_advance_data.xml',
        'security/security.xml',
        'views/hr_payroll_structure_views.xml',
        'views/hr_salary_advance_views.xml',
        'report/hr_salary_advance_report_views.xml',
    ],
    'demo': [],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}

