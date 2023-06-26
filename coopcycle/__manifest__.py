{
    'name': 'Coopcycle',
    'version': '0.1',
    'category': 'Sales/Coopcycle',
    'sequence': 20,
    'summary': 'Connection with Coopcycle',
    'description': "",
    'website': 'https://www.odoo.com/page/crm',
    'depends': [
        'base_setup',
        'account'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/settings.xml',
        'views/coopcycle_views.xml',
        'views/coopcycle_order_query.xml',
        'views/menu_items.xml',
        'views/custom_res_partner_form.xml'
    ],
    'demo': [
    ], 
    'assets': {
        'web.assets_backend': [
            'coopcycle/static/src/views/**/*'
        ]
    },
    'css': [],
    'installable': True,
    'application': True,
    'auto_install': True
}