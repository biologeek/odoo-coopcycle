from odoo import fields, models
from werkzeug.urls import url_join
import requests
import logging
import re
from datetime import datetime,timezone


_logger = logging.getLogger(__name__)

class CoopcycleOrder(models.Model):
    _name = "coopcycle.order"
    _description = "A Coopcycle order"

    api_token = fields.Char(store=False)

    external_id = fields.Integer(string="External ID")
    number = fields.Char(string="Order number")
    items_total = fields.Float(string="Items total")
    total = fields.Float(string="Order total")
    takeaway = fields.Boolean(string="Is takeaway")
    delivery_price_without_taxes = fields.Float(
        string="Delivery paid by customer")
    delivery_fees_witout_taxes = fields.Float(string="Fees paid by restaurant")
    tip_without_taxes = fields.Float(string="Tip given by customer")
    state = fields.Char(string="Order state")
    created_at = fields.Datetime(string="Order created at", help="Datetime at which order was created")
    pickup_expected_at = fields.Datetime(string="Pickup expected at", help="Datetime at which order is picked up at restaurant")
    delivery_expected_at = fields.Datetime(string="Delivery expected at", help="Datetime at which order is delivered to customer")
    delivery_done_at = fields.Datetime(string="Delivery done at", help="Datetime at which order is effectively delivered to customer")
    vendor = fields.Many2one(comodel_name="coopcycle.vendor", string="Order vendor", help="Vendor/Restaurant for the order")
    customer = fields.Many2one(string="Order customer", comodel_name="coopcycle.customer", help="Customer who ordered")
    pickup_address = fields.Many2one(string="Pickup address", comodel_name="coopcycle.address", help="Pickup address")
    delivery_address = fields.Many2one(string="Delivery address", comodel_name="coopcycle.address", help="Delivery address")
    assigned_to = fields.Char(string="Courier")
    lines = fields.One2many(string="Lignes de commande", comodel_name="coopcycle.order_line", inverse_name="order_id")
    

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

    def _coopcycle_get_token(self):

        api_token = None
        base_url = self.env["ir.config_parameter"].sudo(
        ).get_param('coopcycle.api_url')
        user = self.env["ir.config_parameter"].sudo(
        ).get_param('coopcycle.api_user')
        password = self.env["ir.config_parameter"].sudo(
        ).get_param('coopcycle.api_password')

        if not base_url.endswith("api") and not base_url.endswith("api/") :
            base_url = base_url + "" if base_url[-1] == "/" else "/" + "api/"

        
        #url = "https://a2roo.coopcycle.org/api/login_check"
        url = base_url+"/login_check"

        test_url = base_url+ "" if base_url[-1] == "/" else "/"+ "me"

        body = {
            "_username": user,
            "_password": password
        }

        if api_token :
            response = requests.get(url=test_url, headers={'Authorization': 'Bearer '+api_token})
            if response.status_code == "401" :
                api_token = None

        if not api_token:
            response = requests.post(
                url=url,
                headers={'content-type': 'application/json'},
                json=body
            )

            if response.ok : 
                api_token = response.json()["token"]
                return api_token
            else :
                raise Exception("Could not connect to Coopcycle")
            

    def _coopcycle_order_import_request(self, endpoint, params, payload=None, method="GET"):
        api_token = self._coopcycle_get_token()

        base_url = self.env["ir.config_parameter"].sudo(
        ).get_param('coopcycle.api_url')
        url = base_url+ ("" if base_url[-1] == "/" else "/") + endpoint
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer '+api_token
            }

        if method == "GET":
            response = requests.get(url=url, headers=headers, params=params)
        elif method == "POST": 
            response = requests.post(url=url, headers=headers, data=payload)

        if response.ok :

            resp_body = response.json()

            for order in resp_body['hydra:member']: 
                self.create_or_update_record(order)
        else : 
            raise Exception("Error during Coopcycle order request")


    def create_or_update_record(self, order):
        _logger.info("-----------------------")
       #SOMETHING TODO HERE
        result = self.search(domain=[('number', '=', order['number'])], limit=1)
        if result:
            result.update({
                'number': order['number'],
                'total': float(order['total'])/100,
                'takeaway': order['takeaway'],
                'items_total': float(order['itemsTotal'])/100,
                'delivery_price_without_taxes': float(order['adjustments']['delivery'][0]['amount'])/100/1.2 if order['adjustments']['delivery'] and order['adjustments']['delivery'][0]['amount'] else 0,
                'tip_without_taxes': float(order['adjustments']['tip'][0]['amount'])/100/1.2 if order['adjustments']['tip'] and order['adjustments']['tip'][0]['amount'] else 0.0,
                'state': order['state'],
                'pickup_expected_at': datetime.strptime(order['pickupExpectedAt'].replace('T', ' '), '%Y-%m-%d %H:%M:%S%z').replace(tzinfo=timezone.utc).astimezone(tz=None).strftime("%Y-%m-%d %H:%M:%S") if order['pickupExpectedAt'] else None,
                'delivery_expected_at': datetime.strptime(order['shippingTimeRange'][1].replace('T', ' '), '%Y-%m-%d %H:%M:%S%z').replace(tzinfo=timezone.utc).astimezone(tz=None).strftime("%Y-%m-%d %H:%M:%S") if order['shippingTimeRange'] else None,
                'vendor': self.env['coopcycle.vendor'].create_or_update_record(order['restaurant']) if order['restaurant'] else None,
                'customer': self.env['coopcycle.customer'].create_or_update_record(order['customer']),
                'lines': self.env['coopcycle.order_line'].create_or_update_records(order['items'] if order['items'] and len(order['items'])>0 else None, result)
            })
        else:
            #_logger.info({
            #    'id': order['@id'].replace('/api/orders/',''),
            #    'number': order['number'],
            #    'total': float(order['total']),
            #    'items_total': float(order['itemsTotal']),
            #    'takeaway': order['takeaway'],
            #    'delivery_price_without_taxes': float(order['adjustments']['delivery'][0]['amount'])/100/1.2 if order['adjustments']['delivery'] and order['adjustments']['delivery'][0]['amount'] else 0,
            #    'delivery_fees_witout_taxes': None,
            #    'tip_without_taxes': float(order['adjustments']['tip'][0]['amount'])/100/1.2 if order['adjustments']['tip'] and order['adjustments']['tip'][0]['amount'] else 0.0,
            #    'state': order['state'],
            #    'created_at': re.sub('\+([0-9]{2})\:([0-9]{2})','', order['createdAt'].replace('T', ' ')),
            #    'pickup_expected_at': re.sub('\+([0-9]{2})\:([0-9]{2})','', order['pickupExpectedAt'].replace('T', ' ')) if order['pickupExpectedAt'] else None,
            #    'delivery_expected_at': re.sub('\+([0-9]{2})\:([0-9]{2})','', order['shippingTimeRange'][1].replace('T', ' ')) if order['shippingTimeRange'] else None,
            #    'delivery_done_at': None,
            #    'vendor': order['vendor'],
            #    'customer': order['customer'],
            #    'pickup_address': order['restaurant']['address'] if order['restaurant'] else None,
            #    'delivery_address': order['shippingAddress'],
            #    'assigned_to' : order['assignedTo']
            #})
            #_logger.info(order['adjustments']['tip'])
            #_logger.info(order['adjustments']['tip'][0])
            #_logger.info(order['adjustments']['delivery'])
            created = self.env['coopcycle.order'].create({
                'id': order['@id'].replace('/api/orders/',''),
                'number': order['number'],
                'total': float(order['total'])/100,
                'items_total': float(order['itemsTotal'])/100,
                'takeaway': order['takeaway'],
                'delivery_price_without_taxes': float(order['adjustments']['delivery'][0]['amount'])/100/1.2 if order['adjustments'] and order['adjustments']['delivery'] and order['adjustments']['delivery'][0] else 0,
                'delivery_fees_witout_taxes': None,
                'tip_without_taxes': float(order['adjustments']['tip'][0]['amount'])/100/1.2 if order['adjustments']['tip'] and order['adjustments']['tip'][0] else 0.0,
                'state': order['state'],
                'created_at': datetime.strptime(order['createdAt'].replace('T', ' '), '%Y-%m-%d %H:%M:%S%z').replace(tzinfo=timezone.utc).astimezone(tz=None).strftime("%Y-%m-%d %H:%M:%S"),
                'pickup_expected_at': datetime.strptime(order['pickupExpectedAt'].replace('T', ' '), '%Y-%m-%d %H:%M:%S%z').replace(tzinfo=timezone.utc).astimezone(tz=None).strftime("%Y-%m-%d %H:%M:%S") if order['pickupExpectedAt'] else None,
                'delivery_expected_at': datetime.strptime(order['shippingTimeRange'][1].replace('T', ' '), '%Y-%m-%d %H:%M:%S%z').replace(tzinfo=timezone.utc).astimezone(tz=None).strftime("%Y-%m-%d %H:%M:%S") if order['shippingTimeRange'] else None,
                'delivery_done_at': None,
                'vendor': self.env['coopcycle.vendor'].create_or_update_record(order['restaurant']).id if order['restaurant'] else None,
                'customer': self.env['coopcycle.customer'].create_or_update_record(order['customer']).id,
                'pickup_address': self.env['coopcycle.address'].create_or_update_record(order['restaurant']['address']).id if order['restaurant'] else None,
                'delivery_address': self.env['coopcycle.address'].create_or_update_record(order['shippingAddress']).id if order['shippingAddress'] else None,
                'assigned_to' : order['assignedTo']
            })
            self.env['coopcycle.order_line'].create_or_update_records(order['items'] if order['items'] and len(order['items'])>0 else None, created),
