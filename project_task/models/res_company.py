from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    dynamic_task_enabled = fields.Boolean("Enable Dynamic Task", default=False)
    dynamic_task_id = fields.Many2one('res.company.dynamic.task', string="Dynamic Task List")




