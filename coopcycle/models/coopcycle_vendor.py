from odoo import fields, models
import logging

_logger = logging.getLogger(__name__)


class CoopcycleVendor(models.Model):
    _name = "coopcycle.vendor"
    _description = "A Coopcycle vendor"
    _rec_names_search = ['name']
    _rec_name = 'name'


    external_id = fields.Integer(string="External ID")
    name = fields.Char(string="Name")
    phone = fields.Char(string="phone")
    image = fields.Char(string="Front picture")
    stripe_account_id = fields.Char(string="Stripe account ID")
    res_partner_id = fields.Many2one(string="Corresponding ResPartner ID", comodel_name="res.partner")

    
    def create_or_update_record(self, updated) :
        """
        Create or update a Customer record 
        """
        external_id = updated['@id'].replace('/api/restaurants/','')
        result = self.search(domain=[('external_id', '=', external_id)], limit=1)
        #print(result)
        #print("create_or_update_record. Updated ext ID : "+ str(external_id) + " - Result : " +str(result["external_id"]))
        if result:
            _logger.debug("Found vendor with ID "+str(result['id'])+" - ext: "+str(result["external_id"])+" - "+external_id)
            updated = {
                'name': updated['name'],
                'phone': updated['address']['telephone']
            }
            result.update(updated)
            return result
        else : 
            _logger.debug("No vendor found for ID "+external_id)

            return self.create({
                'external_id': external_id,
                'name': updated['name'],
                'phone': updated['address']['telephone']
            })
