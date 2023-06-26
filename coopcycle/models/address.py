from odoo import fields, models



class CoopcycleAddress(models.Model):
    _name = "coopcycle.address"
    _description = "A Coopcycle address"


    streetAddress = fields.Char(string="street address")
