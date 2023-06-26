from odoo import fields, models



class CoopcycleVendor(models.Model):
    _name = "coopcycle.vendor"
    _description = "A Coopcycle vendor"


    id = fields.Integer(string="Id")
    name = fields.Char(string="Name")
    address = fields.Char(string="address")
    phone = fields.Char(string="phone")
    stripe_account_id = fields.Char(string="Stripe account ID")
    res_partner_id = fields.Many2one(string="Corresponding ResPartner ID", comodel_name="res.partner")

