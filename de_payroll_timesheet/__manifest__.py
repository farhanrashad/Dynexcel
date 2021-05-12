# -*- coding: utf-8 -*-
{
    'name': "Payroll Timesheet",

    'summary': """
        Payroll Timesheet
        """,

    'description': """
       Payroll Timesheet
    """,

    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",

    'category': 'Human Resource',
    'version': '14.0.0.1',

    'depends': ['base','hr_payroll'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/hr_contract_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}