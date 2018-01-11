# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Stock Picking Print By Proxy",
    "version": "8.0.1.0.0",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "proxy_backend",
        "stock",
        "stock_transport_multi_address",
        "product_brand"
    ],
    "data": [
        "views/stock_picking_print_proxy.xml"
    ],
    'qweb':[
        'static/src/xml/stock_picking_template.xml',
    ],
}
