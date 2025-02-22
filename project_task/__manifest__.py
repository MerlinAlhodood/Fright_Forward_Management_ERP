# -*- coding: utf-8 -*-
{
    'name': 'Project Task',
    'version': '17.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Project Task',
    'description': 'Task Setting',
    'depends': [
        'hr', 'project','base','project_task_default_stage','account_accountant','fleet'
    ],
    'data': [
        # 'data/ir_sequence.xml',
        # 'security/security.xml',
        'security/ir.model.access.csv',
        'views/project_task.xml',
        'views/res_company.xml',
        'views/fleet_vehicle.xml',
        # 'views/employee_objective.xml',
        # 'views/assign_objective.xml',
        # 'wizard/reject_reason.xml',
        # 'wizard/employee_acheivement_wizard.xml'
    ],
    'assets': {},
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
