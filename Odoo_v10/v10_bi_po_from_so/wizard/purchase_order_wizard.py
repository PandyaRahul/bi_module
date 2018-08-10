# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time
from odoo import api, fields, models, _
from datetime import datetime
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError


class createpurchaseorder(models.TransientModel):
	_name = 'create.purchaseorder'
	_description = "Create Purchase Order"

	new_order_line = fields.One2many( 'getsale.orderdata', 'new_order_line_id',String="Order Line")
	partner_id = fields.Many2one('res.partner', string='Vender', required = True)
	order_date = fields.Date(string="Order Date", default = datetime.today(), required = True)
	state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
        ], string='Status', readonly=True, index=True, copy=False, default='draft',
         track_visibility='onchange')
	
	@api.model
	def default_get(self,  default_fields):
		res = super(createpurchaseorder, self).default_get(default_fields)
		#print "===== A ====="
		data = self.env['sale.order'].browse(self._context.get('active_ids',[]))
		update = []
		for record in data.order_line:
			#print "===== B ====="
			update.append((0,0,{
							'product_id' : record.product_id.id,
							'product_uom' : record.product_uom.id,
							'order_id': record.order_id.id,
							'name' : record.name,
							'product_qty' : record.product_uom_qty,
							'price_unit' : record.price_unit,
							'product_subtotal' : record.price_subtotal,
							}))
		res.update({'new_order_line':update})
		#print "===== Update OK=====",update
		return res

	@api.multi
	def action_create_purchase_order(self):
		self.ensure_one()
		#print "============1==========="
		res = self.env['purchase.order'].browse(self._context.get('id',[]))
		#print "============2===========",res
		value = [] 
		for data in self.new_order_line:
			#print "=======create======= ",value
			value.append([0,0,{
								'product_id' : data.product_id.id,
								'name' : data.name,
								'product_qty' : data.product_qty,
								'order_id':data.order_id.id,
								'product_uom' : data.product_uom.id,
								'date_planned' : data.date_planned,
								'price_unit' : data.price_unit,
								}])
			#print "=========create ok======= ",value
		res.create({
						'partner_id' : self.partner_id.id,
						'order_date' : self.order_date,
						'order_line':value,
						'state' : 'draft'
					})
		#print "=======3======= ",res['order_line']
		return res


class Getsaleorderdata(models.TransientModel):
	_name = 'getsale.orderdata'
	_description = "Get Sale Order Data"

	new_order_line_id = fields.Many2one('create.purchaseorder')
		
	product_id = fields.Many2one('product.product', string="Product", required=True)
	name = fields.Char(string="Description", required=True)
	product_qty = fields.Float(string='Quantity', required=True)
	date_planned = fields.Date(string='Scheduled Date', default = datetime.today(), store=True, index=True, required=True)
	product_uom = fields.Many2one('product.uom', string='Product Unit of Measure')
	order_id = fields.Many2one('sale.order', string='Order Reference', required=True, ondelete='cascade', index=True, copy=False)
	price_unit = fields.Float(string='Unit Price', required=True, digits=dp.get_precision('Product Price'))
	product_subtotal = fields.Float(string="Sub Total", compute='_compute_total')
	
	@api.depends('product_qty', 'price_unit')
	def _compute_total(self):
		for record in self:
			record.product_subtotal = record.product_qty * record.price_unit
