# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time
from odoo import api, fields, models, _
from datetime import datetime
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError


class createsaleorder(models.TransientModel):
	_name = 'create.saleorder'
	_description = "Create Sale Order"

	new_order_line = fields.One2many( 'getpurchase.orderdata', 'new_order_line_id',String="Order Line")
	
	partner_id = fields.Many2one('res.partner', string='Customer', required=True)
	order_date = fields.Date(string="Order Date", default = datetime.today(), required=True)
	state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange')
	
	@api.model
	def default_get(self,  default_fields):
		res = super(createsaleorder, self).default_get(default_fields)
		record = self.env['purchase.order'].browse(self._context.get('active_ids',[]))
		update = []
		for record in record.order_line:
			update.append((0,0,{
					'product_id' : record.product_id.id,
					'name' : record.name,
					'product_qty' : record.product_qty,
					'price_unit' : record.price_unit,
					'product_subtotal' : record.price_subtotal,
					'date_planned' : datetime.today(),
				}))
			res.update({'new_order_line':update})
		return res	


	@api.multi
	def action_create_sale_order(self):
		self.ensure_one()
		res = self.env['sale.order'].browse(self._context.get('id',[]))
		value = [] 
		for data in self.new_order_line:
			value.append([0,0,{
								'product_id' : data.product_id.id,
								'name' : data.name,
								'product_uom_qty' : data.product_qty,
								'price_unit' : data.price_unit,
								}])
		res.create({	'partner_id' : self.partner_id.id,
						'order_date' : self.order_date,
						'order_line':value,
						'state' : 'draft'
					})
		return 


class getpurchaseorder(models.TransientModel):
	_name = 'getpurchase.orderdata'
	_description = "Get purchase Order Data"

	new_order_line_id = fields.Many2one('create.saleorder')
	
	product_id = fields.Many2one('product.product', string="Product", required=True)
	name = fields.Char(string="Description", required=True)
	product_qty = fields.Float(string='Quantity', required=True)
	price_unit = fields.Float(string="Unit Price", required = True)
	product_subtotal = fields.Float(string="Sub Total", compute='_compute_total')


	@api.depends('product_qty', 'price_unit')
	def _compute_total(self):
		for record in self:
			record.product_subtotal = record.product_qty * record.price_unit

