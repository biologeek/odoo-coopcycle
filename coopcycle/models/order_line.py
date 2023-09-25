from odoo import fields, models
import requests
import logging

_logger = logging.getLogger(__name__)

class OrderLine(models.Model):
    _name = "coopcycle.order_line"
    _description = "A Coopcycle order line"
    _rec_names_search = ['product', 'external_id']



    external_id = fields.Integer(string="External_id")
    product = fields.Many2one(string="Product", comodel_name="coopcycle.order_product", help="Product")
    quantity = fields.Float(string="Quantity")
    unit_price = fields.Float(string="Unit price")
    total = fields.Float(string="Total")
    taxes = fields.Float(string="Taxes")
    order_id = fields.Many2one(comodel_name="coopcycle.order", string="Associated order")


    def create_or_update_records(self, list, order):
        if not list or len(list) == 0 :
            return []
        
        for element in list :
            self.create_or_update_record(element, order)

    def create_or_update_record(self, record, parent_order):
        result = self.search(domain=[('external_id', '=', record['id'])], limit=1)
        if result:
            result.update({
                'order_id': parent_order.id,
                'product': self.env['coopcycle.order_product'].create_or_update_record_from_item(record).id,
                'quantity': record['quantity'],
                'unit_price': float(record['unitPrice'])/100,
                'total': float(record['total'])/100,
                'taxes': float(record['adjustments']['tax'][0]['amount'])/100 if record['adjustments'] and record['adjustments']['tax'] else 0.0
            })
        else :
            result = self.create({
                'order_id': parent_order.id,
                'product': self.env['coopcycle.order_product'].create_or_update_record_from_item(record).id,
                'quantity': record['quantity'],
                'unit_price': float(record['unitPrice'])/100,
                'total': float(record['total'])/100,
                'taxes': float(record['adjustments']['tax'][0]['amount'])/100 if record['adjustments'] and record['adjustments']['tax'] else 0.0
            })
        return result

