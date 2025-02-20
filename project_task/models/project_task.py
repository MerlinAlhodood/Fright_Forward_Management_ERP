from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class ResCompanyDynamicTask(models.Model):
    _name = 'res.company.dynamic.task'
    _description = 'Dynamic Task for Company'

    name = fields.Char(string="Task Name", required=True)
    task_line_ids = fields.One2many('res.company.dynamic.task.line', 'task_id',
                                    string="Task Lines")



class ResCompanyDynamicTaskLine(models.Model):
    _name = 'res.company.dynamic.task.line'
    _description = 'Lines for Dynamic Task'

    name = fields.Char(string="Line Name", required=True)
    task_id = fields.Many2one('res.company.dynamic.task', string="Task")



class ProjectProject(models.Model):
    _inherit = 'project.project'


    @api.model
    def create(self, vals):
        project = super(ProjectProject, self).create(vals)
        company = self.env.company
        print(company,'companyyyyyyy')
        print(company.dynamic_task_id, 'taskkkkk')
        print(company.dynamic_task_enabled, 'enableeeeeeeeee')

        if company.dynamic_task_enabled and company.dynamic_task_id:
            main_task = self.env['project.task'].create({
                'name': company.dynamic_task_id.name,
                'project_id': project.id,
                'task_line_ids': [
                    (0, 0, {'name': line.name}) for line in company.dynamic_task_id.task_line_ids
                ],
            })
            print(main_task,'main taskkkkkkkk')

        return project





class ProjectTaskLine(models.Model):
    _name = 'project.task.line'
    _description = 'Project Task Line'

    name = fields.Char(string="Check List", required=True)
    task_id = fields.Many2one('project.task', string="Task", ondelete='cascade')
    is_checked = fields.Boolean(string="", default=False)


    stage_type = fields.Selection(
        related='task_id.stage_id.stage_type',
        string="Stage Type",
        store=True
    )

    is_checked_readonly = fields.Boolean(
        string="",
        compute='_compute_is_checked_readonly',

    )

    @api.depends('stage_type')
    def _compute_is_checked_readonly(self):
        for line in self:
            line.is_checked_readonly = line.stage_type == 'completed'





class ProjectTask(models.Model):
    _inherit = 'project.task'

    task_line_ids = fields.One2many('project.task.line', 'task_id', string="Task Lines")
    transfer_type = fields.Selection(
        [
            ('import', 'Import'),
            ('export', 'Export')
        ],
        string="Transfer Type"
    )
    operation = fields.Selection([
        ('direct', 'Direct'),
        ('house', 'House'),
        ('master', 'Master'),
    ], string='Type', required=True, default='direct')

    @api.constrains('stage_id')
    def _check_stage_completion(self):
        for task in self:
            if task.stage_id.stage_type == 'completed':
                unchecked_lines = task.task_line_ids.filtered(lambda line: not line.is_checked)
                if unchecked_lines:
                    raise ValidationError("All checklist items must be checked before moving to the 'Completed' stage.")





