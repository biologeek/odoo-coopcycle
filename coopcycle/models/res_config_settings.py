
from datetime import timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, exceptions, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    coopcycle_api_url = fields.Char(string="API URL", help="Your Coopcycle instance URL", stored=True, readonly=False, config_parameter="coopcycle.api_url")
    coopcycle_api_user = fields.Char(string="API user", help="Your Coopcycle username", config_parameter="coopcycle.api_user", stored=True, readonly=False)
    coopcycle_api_password = fields.Char(string="API password", help="Your Coopcycle password", config_parameter="coopcycle.api_password", stored=True, readonly=False)



