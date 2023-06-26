from odoo import fields, models
from werkzeug.urls import url_join
import requests


class CoopcycleOrder(models.Model):
    _name = "coopcycle.order"
    _description = "A Coopcycle order"

    api_token = None

    id = fields.Integer(string="Id")
    number = fields.Char(string="Order number")
    total = fields.Integer(string="Order total")
    takeaway = fields.Boolean(string="Is takeaway")
    itemsTotal = fields.Float(string="Items total")
    deliveryPriceWitoutTaxes = fields.Float(
        string="Delivery paid by customer")
    deliveryFeesWitoutTaxes = fields.Float(string="Fees paid by restaurant")
    tipWitoutTaxes = fields.Float(string="Tip given by customer")
    state = fields.Char(string="Order state")
    odoo_status = fields.Selection([
        ('imported', 'Imported'),
        ('payment_checked', 'Payment checked'),
        ('integrated', 'Integrated'),
        ('discarded', 'Discarded')
    ], default='imported', required=True, string="Order status in Odoo")

    def action_mark_as_discarded(self):
        self.odoo_status = 'discarded'

    def action_import_coopcycle_orders(self):
        None

    def _coopcycle_order_make_auth(self):
        base_url = self.env["ir.config_parameter"].sudo(
        ).get_param('coopcycle.coopcycle_api_url')
        user = self.env["ir.config_parameter"].sudo(
        ).get_param('coopcycle.coopcycle_api_user')
        password = self.env["ir.config_parameter"].sudo(
        ).get_param('coopcycle.coopcycle_api_password')
        url = url_join(
            base_url, "" if base_url[-1] == "/" else "/", "login_check")

        test_url = url_join(
            base_url, "" if base_url[-1] == "/" else "/", "me")

        body = {
            "_username": user,
            "_password": password
        }

        if self.api_token :
            response = requests.get(url=test_url, headers={'Authorization': 'Bearer '+self.api_token})
            if response.status_code == "401" :
                self.api_token = None

        if not self.api_token:
            response = requests.post(
                url=url,
                headers={'content-type': 'application/json'},
                json=body
            )

            if response.ok : 
                self.api_token = response.json()["token"]
            else :
                raise Exception("Could not connect to Coopcycle")

    def _coopcycle_order_make_request(self, endpoint, params, payload=None, method="GET"):
        self.ensure_one()
        self._coopcycle_order_make_auth()

        base_url = self.env["ir.config_parameter"].sudo(
        ).get_param('coopcycle.coopcycle_api_url')

        url = url_join(base_url, "" if base_url[-1] == "/" else "/", endpoint)

        if method == "GET":
            response = requests.get(url=url, params=params)
        elif method == "POST": 
            response = requests.post(url=url, data=payload)

        if response.ok :
            return response.json
        else : 
            raise Exception("Error during Coopcycle order request")
