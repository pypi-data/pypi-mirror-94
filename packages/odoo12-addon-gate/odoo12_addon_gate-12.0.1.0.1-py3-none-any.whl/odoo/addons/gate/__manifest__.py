{
    'name': "Manage your Gateway for ThingsInTouch Devices",
    'summary': "Receive and send data to your net of sensors and devices",       
    'description': """Receive and send data
        to your net of sensors and devices""",

    'version': '12.0.1.0.1',
    'category': 'Things',
    'website': "http://www.thingsintouch.com",
    'author': "thingsintouch.com",
    'license': 'AGPL-3',
    'application': False,
    'installable': True,    
    'depends': ['base'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/things_menus.xml',
        'views/things_gate.xml',
        'views/popup_wizard.xml',
    ],
# 'demo': ['demo.xml'],
}