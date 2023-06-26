from odoo import fields, models



class Customer(models.Model):
    _name = "coopcycle.customer"
    _description = "A Coopcycle customer"


    fullName = fields.Char(string="Customer name")
