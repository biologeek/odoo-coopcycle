from odoo import fields, models
import logging
#_logger = logging.getLogger(__name__)


class CoopcycleAddress(models.Model):
    _name = "coopcycle.address"
    _description = "A Coopcycle address"
    _rec_names_search = ['street_address']
    _rec_name = 'street_address'

    name = fields.Char(string="Customer name")
    external_id = fields.Integer(string = "External ID")

    contact = fields.Char(string="Contact name")
    street_address = fields.Char(string="street address")
    postal_code = fields.Char(string="Postal code")
    city = fields.Char(string="City")
   
    def create_or_update_record(self, updated) :
        """
        Create or update a Customer record 
        """
        #_logger.info("Updated : "+str(updated))

        external_id = updated['@id'].replace('/api/addresses/','')
        result = self.search(domain=[('external_id', '=', external_id)], limit=1)
        if result:
            result.update({
                'name': updated['name'],
                'street_address': updated['streetAddress']
            })
            return result
        else : 
            return self.create({
                'external_id': external_id,
                'name': updated['name'],
                'street_address': updated['streetAddress']
            })
