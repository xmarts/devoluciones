# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date, time, timedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class fecha_limited(models.Model):
	_inherit = 'sale.order'

	fecha_limit = fields.Date(string="date limtit return")


class opciondevolucion(models.Model):

	_inherit ='stock.picking.type'

	client_devo = fields.Boolean(string="Return client")
	provee_devo =fields.Boolean(string="supplier return")



class devolucion_produ(models.Model):
	_name = 'return.clien'


	tabla = fields.One2many('product.validar', 'tabla_1')

	num_clie = fields.Char(string="Number client")
	nombre_clien =fields.Many2one('res.partner',string="Name client")
	contador = fields.Integer(string="Contador", compute="_get_contador")
	pedido = fields.Char(string="Pedido")
	estado_clien = fields.Many2one('res.country.state',string="State")
	cuidad_clien = fields.Char(string="City")
	codi_pos_clien = fields.Char(string="Postal client")
	fecha_actual = fields.Date(string="Date",default=fields.Date.today())
	busqueda = fields.Char(string="Search series",required=1)
	state = fields.Selection([('draft','Draft'),('approve','Approved'),('review','Review piece'),('state','good condition'),('default','manufacturing'),('process','Processing'),('reject','Rejected')],default='draft')
	rel = fields.Char(string="relacion")
	tipo_devo = fields.Selection([('cl','Cliente'),('de','Proveedor')],string="type of returns")
	name_canceled = fields.Many2one('res.users',string="name of who canceled", readonly=True)
	total_acept  = fields.Integer(string="Total aceptados", compute="_total_devoluciones")
	total_recha = fields.Integer(string="Total rechazados")

	@api.one
	def buscar(self):
		if self.tipo_devo == 'cl':
			obj_serie = self.env['stock.move.line'].search([('lot_id', '=', self.busqueda)], limit=1)
			obj_order = self.env['stock.picking'].search([('name', '=', obj_serie.reference)], limit=1)
			dev = self.env['sale.order'].search([('name','=',obj_order.origin,)],limit=1)
			if obj_order:
				if self.pedido:
					self.pedido = self.pedido
				else:
					self.pedido = obj_order.origin		
			if obj_order.picking_type_code == 'outgoing':

				if  dev.fecha_limit > self.fecha_actual :	
					if obj_serie:	
						obj_table = self.env['product.validar']
						if self.tabla:
							con = 0
							for line in self.tabla:
								if obj_serie.lot_id == line.serie:
									con += 1
								else:
									con = 0
							if con ==0 :	
								obj_line = obj_table .create({'producto': obj_serie.product_id.id,
														'serie':obj_serie.lot_id.id,
														'cantidad': obj_serie.qty_done,
														'fecha_compra': obj_serie.date,
														'pedido_venta':obj_order.origin,
														'estatus':obj_serie.state,
														'tabla_1': self.id,
														})
								if obj_line:
									datos = self.env['stock.picking'].search([('name', '=', obj_serie.reference)], limit=1)
									self.nombre_clien = datos.partner_id.id 
									self.cuidad_clien = datos.partner_id.city
									self.estado_clien = datos.partner_id.state_id.id
									self.codi_pos_clien = datos.partner_id.zip
							else:
								raise UserError('La serie que intenta buscar ya se encuentra en la tabla')
						else:
							obj_line = obj_table .create({'producto': obj_serie.product_id.id,
															'serie':obj_serie.lot_id.id,
															'cantidad': obj_serie.qty_done,
															'fecha_compra': obj_serie.date,
															'pedido_venta':obj_order.origin,
															'estatus':obj_serie.state,
															'tabla_1': self.id,
															})
							if obj_line:
								datos = self.env['stock.picking'].search([('name', '=', obj_serie.reference)], limit=1)
								self.nombre_clien = datos.partner_id.id 
								self.cuidad_clien = datos.partner_id.city
								self.estado_clien = datos.partner_id.state_id.id
								self.codi_pos_clien = datos.partner_id.zip			
					else:
						raise ValidationError('No se encontro una serie con este nombre, por favor intenta con otra.')
				else:
					if obj_serie:	
						obj_table = self.env['product.validar']
						if self.tabla:
							con = 0
							for line in self.tabla:
								if obj_serie.lot_id == line.serie:
									con += 1
								else:
									con = 0
							if con ==0 :	
								obj_line = obj_table .create({'producto': obj_serie.product_id.id,
														'serie':obj_serie.lot_id.id,
														'cantidad': obj_serie.qty_done,
														'fecha_compra': obj_serie.date,
														'pedido_venta':obj_order.origin,
														'estatus':obj_serie.state,
														'tabla_1': self.id,
														})
								if obj_line:
									datos = self.env['stock.picking'].search([('name', '=', obj_serie.reference)], limit=1)
									self.nombre_clien = datos.partner_id.id 
									self.cuidad_clien = datos.partner_id.city
									self.estado_clien = datos.partner_id.state_id.id
									self.codi_pos_clien = datos.partner_id.zip
							else:
								raise UserError('La serie que intenta buscar ya se encuentra en la tabla')
						else:
							obj_line = obj_table .create({'producto': obj_serie.product_id.id,
															'serie':obj_serie.lot_id.id,
															'cantidad': obj_serie.qty_done,
															'fecha_compra': obj_serie.date,
															'pedido_venta':obj_order.origin,
															'estatus':obj_serie.state,
															'tabla_1': self.id,
															})
							if obj_line:
								datos = self.env['stock.picking'].search([('name', '=', obj_serie.reference)], limit=1)
								self.nombre_clien = datos.partner_id.id 
								self.cuidad_clien = datos.partner_id.city
								self.estado_clien = datos.partner_id.state_id.id
								self.codi_pos_clien = datos.partner_id.zip	
					self.write({'state':'reject'})
					self.name_canceled = self.env.user.id			
						
			else:
				raise ValidationError('Esta serie pertenece a una compra')							
	
     ########## parte del funcionamiento para compras   ##############################			
		else :
			if self.tipo_devo == 'de':
				obj_serie = self.env['stock.move.line'].search([('lot_id', '=', self.busqueda)], limit=1)
				obj_order = self.env['stock.picking'].search([('name', '=', obj_serie.reference)], limit=1)
				pur = self.env['purchase.order'].search([('name','=',obj_order.origin,)],limit=1)
				if obj_order:
					if self.pedido:
						self.pedido = self.pedido
					else:
						self.pedido = obj_order.origin		
				if obj_order.picking_type_code == 'incoming':
					if obj_serie:	
						obj_table = self.env['product.validar']
						if self.tabla:
							con = 0
							for line in self.tabla:
								if obj_serie.lot_id == line.serie:
									con += 1
								else:
									con = 0
							if con ==0 :	
								obj_line = obj_table .create({'producto': obj_serie.product_id.id,
														'serie':obj_serie.lot_id.id,
														'cantidad': obj_serie.qty_done,
														'fecha_compra': obj_serie.date,
														'pedido_venta':obj_order.origin,
														'estatus':obj_serie.state,
														'tabla_1': self.id,
														})
								if obj_line:
									datos = self.env['stock.picking'].search([('name', '=', obj_serie.reference)], limit=1)
									self.nombre_clien = datos.partner_id.id 
									self.cuidad_clien = datos.partner_id.city
									self.estado_clien = datos.partner_id.state_id.id
									self.codi_pos_clien = datos.partner_id.zip
							else:
								raise UserError('La serie que intenta buscar ya se encuentra en la tabla')
						else:
							obj_line = obj_table .create({'producto': obj_serie.product_id.id,
															'serie':obj_serie.lot_id.id,
															'cantidad': obj_serie.qty_done,
															'fecha_compra': obj_serie.date,
															'pedido_venta':obj_order.origin,
															'estatus':obj_serie.state,
															'tabla_1': self.id,
															})
							if obj_line:
								datos = self.env['stock.picking'].search([('name', '=', obj_serie.reference)], limit=1)
								self.nombre_clien = datos.partner_id.id 
								self.cuidad_clien = datos.partner_id.city
								self.estado_clien = datos.partner_id.state_id.id
								self.codi_pos_clien = datos.partner_id.zip
									
					else:
						raise ValidationError('No se encontro una serie con este nombre, por favor intenta con otra.')
				else:
					raise ValidationError('Esta serie pertenece a una venta')		
				

	@api.depends('tabla')
	def _total_devoluciones(self):
		devoluciones = 0
		for orde in self.tabla:
			devoluciones += orde.cant_devo
			self.total_acept = devoluciones

	@api.one
	def dra(self):
		self.write({'state':'draft'})

	@api.depends('tabla.pedido_venta')
	def _get_contador(self):
		suma = 0
		for var in self:
			for line in var.tabla:
				if line.pedido_venta != self.pedido:
					suma += 1
					self.contador = suma
				else:
					self.contador = suma	
					

	@api.one
	def confirmar(self,):
		obj_serie = self.env['stock.move.line'].search([('lot_id', '=', self.busqueda)], limit=1)
		obj_order = self.env['stock.picking'].search([('name', '=', obj_serie.reference)], limit=1)
		if self.contador == 0:
			if obj_order.picking_type_code == 'outgoing':
				pick_t_id = self.env['stock.picking.type'].search([('client_devo','=',True)])
				obj_order.write({'picking_type_id':pick_t_id.return_picking_type_id.id})
				self.write({'state':'approve'})
			else:
				pick_t_id = self.env['stock.picking.type'].search([('provee_devo','=',True)])
				obj_order.write({'picking_type_id':pick_t_id.return_picking_type_id.id})
				self.write({'state':'approve'})
		else:
			raise ValidationError('Existen productos que no pertenecen al mismo pedido, por favor verifique los productos')	

	@api.one
	def rev(self):
		self.write({'state':'review'})

	@api.one
	def ste(self):
		self.write({'state':'state'})

	@api.one
	def defa(self):
		self.write({'state':'default'})
	@api.one
	def proce(self):
		self.write({'state':'process'})

	@api.one
	def rej(self):
		self.write({'state':'reject'})

		


class tabla(models.Model):
	_name= 'product.validar'

	tabla_1 = fields.Many2one('return.clien',ondelete='cascade')
	producto = fields.Many2one('product.product',string="Product")
	talla  = fields.Char(string="Talla")
	cantidad = fields.Float(string="cantidad")
	serie = fields.Many2one('stock.production.lot',string="Serie")
	pedido_venta = fields.Char(string="Pedido")
	fecha_compra = fields.Datetime(string="Fecha")
	estatus = fields.Char(string="Estatus")
	motivo = fields.Char(string="Motivo")
	pregresar_proveedor = fields.Boolean(string="Regresar ", default=False)
	cant_devo = fields.Float(string="cantidad a devolver")
