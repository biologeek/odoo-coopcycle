from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)

class Customer(models.Model):
    _name = "coopcycle.customer"
    _description = "A Coopcycle customer"
    _rec_names_search = ['full_name']
    _rec_name = 'full_name'

    external_id = fields.Integer(string="External ID")
    full_name = fields.Char(string="Customer name")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone number")
    orders = fields.One2many(string="Orders", comodel_name="coopcycle.order", inverse_name="customer")
    order_count = fields.Integer(string="Order count", compute="_compute_order_count", store=True, readonly=False, precompute=True)



    @api.depends('orders')
    def _compute_order_count(self):
        for c in self:
            _logger.info("Computing for "+str(c.id))
            c.order_count = self.env["coopcycle.order"].search_count(domain=[('customer', '=', c.id)])
            _logger.info("Found "+str(c.order_count))

    def create_or_update_record(self, updated) :
        """
        Create or update a Customer record 
        """
        external_id = updated['@id'].replace('/api/customers/','')
        result = self.search(domain=[('external_id', '=', external_id)], limit=1)
        if result:
            result.update({
                'full_name': updated['fullName'],
                'email': updated['email'],
                'phone': updated['phoneNumber'],
                'order_count': self._compute_order_count()
            })
            return result
        else : 
            return self.create({
                'external_id': external_id,
                'full_name': updated['fullName'],
                'email': updated['email'],
                'phone': updated['phoneNumber']
            })
