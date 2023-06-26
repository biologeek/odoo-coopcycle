from odoo import fields, models



class CoopcycleResPartner(models.Model):
    _name = "res.partner"
    _description = "A Coopcycle and Stripe ready Partner"
    _inherit = "res.partner"


    stripe_account_id = fields.Char(string="Stripe account ID", help="Provide account ID in the form acct_aAbBcCdD1234")



