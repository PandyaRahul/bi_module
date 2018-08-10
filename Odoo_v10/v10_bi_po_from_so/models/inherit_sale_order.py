# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError,ValidationError


class saleorder(models.Model):
	_inherit = 'sale.order'
	_description = "Sale Order"
	