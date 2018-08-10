# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name'          :   'SO From PO ',

    'summary'       :   'Genarate Sale Order from Purchase Order',

    'author'        :   'BrowseInfo',
    
    'company'       :   'BrowseInfo',
    'category'      :   'Tools',
    'version'       :   '10.0.0.1',
    'description'   :   ''' Genarate Sale Order from Purchase Order ''',
    'website'       :   'https://www.browseinfo.in',
    'depends'       :   [ 'base','product', 'sale','purchase'],
    'license'       :   'OPL-1',
    
    'data'          :   [
                            'wizard/sale_order_wizard_view.xml',
                            'views/main_purchase_order_view.xml',
                        ],      

    'test'          :   [ ],
    'css'           :   [ ],

    'demo'          :   [ ],

    'installable'   :   'True',
    'application'   :   'False',
    'application'   :   False,
}
