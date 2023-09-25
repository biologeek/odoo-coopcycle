from odoo import fields, models
import logging

_logger = logging.getLogger(__name__)

class CoopcycleTask(models.Model):
    _name = "coopcycle.task"
    _description = "A Coopcycle task"

    external_id = fields.Integer(string="Coopcycle ID")
    status = fields.Char(string="Task status")
    created_at = fields.Datetime(string="Creation date")
    weight = fields.Float(string="Weight")
    after = fields.Datetime(string="Deliver after")
    before = fields.Datetime(string="Deliver before")
    comments = fields.Char(string="Comments")
    
