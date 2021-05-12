# -*- coding: utf-8 -*-
{
    'name': "Employee Disciplinary Action",

    'summary': """
         Employee Desciplinary Case
         1-This module depends on Employee app
         """,

    'description': """
        Disciplinary Action
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Employee',
    'version': '14.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr_contract','hr_payroll'],

    # always loaded
    'data': [
        'report/disciplinary_case_report.xml',
        'report/disciplinary_case_template.xml',
        'data/desciplinary_case_seq.xml',
        'data/mail_template_data.xml',
        'security/ir.model.access.csv',
        'views/desciplinary_case_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
