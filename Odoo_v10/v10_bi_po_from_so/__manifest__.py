# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name'          :   'PO From SO ',

    'summary'       :   'Genarate Purchase Order from Sale Order',

    'author'        :   'BrowseInfo',
    
    'company'       :   'BrowseInfo',
    'category'      :   'Tools',
    'version'       :   '10.0.0.1',
    'description'   :   ''' Genarate Purchase Order from Sale Order ''',
    'website'       :   'https://www.browseinfo.in',
    'depends'       :   [ 'base', 'product', 'sale','purchase'],
    'license'       :   'OPL-1',
    
    'data'          :   [
                            'wizard/purchase_order_wizard_view.xml',
                            'views/inherit_sale_order_view.xml',
                        ],

    'test'          :   [ ],
    'css'           :   [ ],
    'demo'          :   [ ],

    'installable'   :   'True',
    'application'   :   'False',
    'application'   :   False,
}
