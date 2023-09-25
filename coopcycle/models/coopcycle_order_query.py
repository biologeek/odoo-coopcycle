# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, fields, models
from odoo.osv import expression
from odoo.tools.misc import format_datetime
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)

class CoopcycleOrderQuery(models.TransientModel):
    _name = 'coopcycle.order.query'
    _description = 'Coopcycle Order Query'

    begin = fields.Datetime('Begin date',
        help="Choose a date to get the orders from that date",
        default=fields.Datetime.now)

    end = fields.Datetime('End date',
        help="Choose a date to get the orders until that date",
        default=fields.Datetime.now)

    def open_for_dates(self):

        tree_view_id = self.env.ref('coopcycle.coopcycle_order_tree_view').id
        form_view_id = self.env.ref('coopcycle.coopcycle_order_form_view').id
        
        for date in [self.begin+timedelta(days=x) for x in range((self.end-self.begin).days)] :

            self.env['coopcycle.order']._coopcycle_order_import_request("orders", {'date': date.strftime("%Y-%m-%d")})
           

        
        return {
            'type': 'ir.actions.act_window',
            'views': [(tree_view_id, 'tree'), (form_view_id, 'form')],
            'view_mode': 'tree,form',
            'name': _('Coopcycle orders'),
            'res_model': 'coopcycle.order',
            'domain': None,
            'context': dict(self.env.context, begin=self.begin, end=self.end),
        }
