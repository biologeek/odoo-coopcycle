from odoo import fields, models
import requests
import logging

_logger = logging.getLogger(__name__)

class OrderProduct(models.Model):
    _name = "coopcycle.order_product"
    _description = "A Coopcycle order product"
    _rec_names_search = ['name', 'external_id']



    external_id = fields.Integer(string="External_id")
    name = fields.Char(string="Product name")
    description = fields.Char(string="Product description")
    price = fields.Float(string="Price")
    taxes = fields.Float(string="Taxes")


    def create_or_update_records(self, list):
        if not list or len(list) == 0 :
            return []
        
        for element in list :
            self.create_or_update_record(element)

    def create_or_update_record_from_item(self, record):


        result = self.search(domain=[('name', '=', record['name']), ('price', '=', float(record['unitPrice'])/100)], limit=1)

        if result:
            result.update({
                'name': record['name'],
                'price': float(record['unitPrice'])/100,
                'taxes': float(record['adjustments']['tax'][0]['amount'])/record['quantity']/100 if record['adjustments'] and record['adjustments']['tax'] else 0.0
            })
            return result
        else :
            return self.create({
                'name': record['name'],
                'price': float(record['unitPrice'])/100,
                'taxes': float(record['adjustments']['tax'][0]['amount'])/record['quantity']/100 if record['adjustments'] and record['adjustments']['tax'] else 0.0
            })

