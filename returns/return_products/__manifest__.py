# -*- coding: utf-8 -*-
{
    'name': "return_products",

    'summary': 
    """In this module returns are made for purchases and sales,
    generating a series of states to approve the return of productsm""",

    'description': """
   In this module returns are made for purchases and sales, generating a series of states to approve the return of products,
   where sales has a functionality that allows you to reject the product by return time and sending the name of the user who is making the return.
    """,

    'author': "XMARTS",
    'email' :"desarrollo@xmarts.com",
    'contributors':"luis angel gonzalez cruz",
    
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'tickets/ticket_cl.xml',
        'tickets/ticket_cl_temp.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application':True,
    'installable':True
}