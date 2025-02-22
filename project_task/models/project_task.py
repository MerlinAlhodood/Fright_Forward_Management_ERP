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

    created_date = fields.Datetime(string="Create Date")
    quot_id = fields.Char(string="Quotation")

    transport = fields.Selection(
        [
            ('air', 'Air'),
            ('ocean', 'Ocean'),
            ('land', 'Land')
        ],
        string="Transport Via"
    )

    in_land_shipment_type = fields.Selection(
        [
            ('ftl', 'Full Truckload(FTL)'),
            ('ltl', 'Less than Truckload(LTL)')

        ],
        string="Land Shipment"
    )

    address_to = fields.Selection(
        [
            ('sc_address', 'Contact Address'),
            ('location_address', 'Location Address')

        ],
        string="Land Shipment"
    )
    shipper_id = fields.Many2one('res.partner', string="Shipper", required=True)
    shipper_phone = fields.Char(string="")
    shipper_email = fields.Char(string="")

    s_street = fields.Char(string="Street", help="Address Line 1")
    s_street2 = fields.Char(string="Street 2", help="Address Line 2")
    s_city = fields.Char(string="City", help="City")
    s_state_id = fields.Many2one('res.country.state', string="State", help="State")
    s_zip = fields.Char(string="ZIP", help="ZIP Code")
    s_country_id = fields.Many2one('res.country', string="Country", help="Country")





    consignee_id = fields.Many2one('res.partner', string="Consignee", required=True)
    consignee_phone = fields.Char(string="")
    consignee_email=fields.Char(string="")

    first_notify_id = fields.Many2one('res.partner', string="1st Notify", required=True)
    final_destination_id = fields.Char(string="Final Destination")
    second_notify_id = fields.Many2one('res.partner', string="2nd Notify", required=True)

    truck_ref = fields.Char(string="CMR/RWB")
    trucker= fields.Char(string="Vehicle")
    truck_owner_id= fields.Many2one('res.partner',string="Owner")
    trucker_number= fields.Char(string="Reference")

    pickup_datetime = fields.Datetime(string="Estimate Pickup Time")
    arrival_datetime = fields.Datetime(string="Estimate Arrival Time")

    approx_charges = fields.Monetary(string="Approx Quotation Charges", currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    distance = fields.Integer(string="Distance(KM)")

    length = fields.Float(string="Length (cm)")
    width = fields.Float(string="Width (cm)")
    height = fields.Float(string="Height (cm)")
    weight = fields.Float(string="Weight (kg)")

    tracking_number = fields.Char(string="Tracking Number")
    barcode = fields.Char(string="Barcode")
    agent_id = fields.Many2one('res.partner', string="Agent")
    operator_id = fields.Many2one('res.users', string="Responsible")
    notes = fields.Text(string="Notes")

    move_type = fields.Char(string="Move Type")
    incoterm = fields.Char(string="Incoterm")
    dangerous_goods = fields.Boolean(string="Dangerous Goods")
    dangerous_goods_notes = fields.Text(string=" Notes")

    cargo_desc = fields.Text(string="Cargo Description")
    commodity = fields.Text(string="Commodity")

    freight_collect_prepaid = fields.Selection(
        [
            ('collect', 'Collect'),
            ('prepaid', 'Prepaid')
        ],
        string="Bill",
        required=True,
        default='prepaid'
    )
    no_of_containers = fields.Integer(string="No of Containers")
    container_size = fields.Char(string="Container Size")
    container_type = fields.Selection(
        [
            ('dry', 'Collect'),
            ('reefer', 'Reefer'),
            ('flat_rock', 'Flat Rock'),
            ('open_top', 'Open Top'),
            ('other', 'Other'),
        ],
        string="Container Type",
        required=True,
    )

    mask_numbers = fields.Text(string="Mask & Numbers")
    hs_code = fields.Char(string="HS COde")
    bl_document_type = fields.Selection(
        [
            ('draft', 'Draft'),
            ('copy', 'Copy'),
            ('original', 'Original'),
            ('telex release', 'Telex Release')
        ],
        string="B/L Document Type",
        required=True,
    )
    total_weight = fields.Char(string="Total Weight")
    gross_weight = fields.Char(string="Gross Weight")
    temperature = fields.Char(string="Temperature")
    humidity = fields.Char(string="Humidity")
    ventilation = fields.Char(string="Ventilation")






    @api.onchange('shipper_id')
    def _onchange_shipper(self):
        if self.shipper_id:
            self.shipper_phone = self.shipper_id.phone or ''
            self.shipper_email = self.shipper_id.email or ''
        else:
            self.shipper_phone = ''
            self.shipper_email = ''

    @api.onchange('consignee_id')
    def _onchange_consignee(self):
        if self.consignee_id:
            self.consignee_phone = self.consignee_id.phone or ''
            self.consignee_email = self.consignee_id.email or ''
        else:
            self.consignee_phone = ''
            self.consignee_email = ''










    @api.constrains('stage_id')
    def _check_stage_completion(self):
        for task in self:
            if task.stage_id.stage_type == 'completed':
                unchecked_lines = task.task_line_ids.filtered(lambda line: not line.is_checked)
                if unchecked_lines:
                    raise ValidationError("All checklist items must be checked before moving to the 'Completed' stage.")





