from odoo import fields, models



class StripeOperation(models.Model):
    _name = "coopcycle.stripe"
    _description = "A Stripe operation"
    


    account_id = fields.Char(string="Stripe account ID", help="coucou")



