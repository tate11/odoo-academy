import odoorpc

# Prepare the connection to the server
odoo = odoorpc.ODOO('localhost', port=50110)

# Login
odoo.login('odoo_50110_dev_academy', 'admin', 'admin')

module = odoo.env.ref('base.module_academy_base')

print(module.button_immediate_upgrade())
#print(dir(odoo.env['ir.ui.view']))
