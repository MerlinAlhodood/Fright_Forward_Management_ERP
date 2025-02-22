from odoo import models, fields, api


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    analytic_account_new = fields.Many2one('account.analytic.account', string="Analytic Account", readonly=True)

    @api.model
    def create(self, vals):
        vehicle = super(FleetVehicle, self).create(vals)

        analytic_account = self.env['account.analytic.account'].create({
            'name': vehicle.name,
            'company_id': vehicle.company_id.id if vehicle.company_id else self.env.company.id,
        })


        vehicle.analytic_account_id = analytic_account.id

        return vehicle
