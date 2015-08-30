from django.db import models

# Create your models here.

class Company( models.Model ):

	name		= models.CharField( max_length = 50 )

	def __str__( self ):
		return "%s" % ( self.name )
	
	class Meta:
		verbose_name_plural = u"Companies"

class Country( models.Model ):

	name		= models.CharField( max_length = 50 )
	iso_code	= models.CharField( max_length = 2 )

	def __str__( self ):
		return "%s" % ( self.iso_code )
	
	class Meta:
		verbose_name_plural = u"Countries"

class City( models.Model ):

	country		= models.ForeignKey( Country )
	name		= models.CharField( max_length = 50 )

	def __str__( self ):
		return "%s - %s" % ( self.country.iso_code , self.name )
	
	class Meta:
		verbose_name_plural = u"Cities"

class Building( models.Model ):

	city		= models.ForeignKey( City )
	name		= models.CharField( max_length = 50 )

	def __str__( self ):
		return "%s - %s" % ( self.city , self.name )
	
	class Meta:
		verbose_name_plural = u"Buildings"

class DataCenterRoom( models.Model ):

	building	= models.ForeignKey( Building )
	name		= models.CharField( max_length = 50 )
	
	def get_absolute_url(self):
		return "/dc/" + str(self.id) + "/"

	def __str__( self ):
		return "%s - %s" % ( self.building , self.name )
	
	class Meta:
		verbose_name_plural = u"Data center rooms"

class Row( models.Model ):

	datacenterroom		= models.ForeignKey( DataCenterRoom )
	name		= models.CharField( max_length = 50 )
	
	def get_absolute_url(self):
		return "/row/" + str(self.id) + "/"

	def __str__( self ):
		return "%s - %s" % ( self.datacenterroom , self.name )
	
	class Meta:
		verbose_name_plural = u"Rows"

class Cabinet( models.Model ):

	row			= models.ForeignKey( Row )
	name		= models.CharField( max_length = 50 )
	
	def get_absolute_url(self):
		return "/cabinet/" + str(self.id) + "/"

	def __str__( self ):
		return "%s - %s" % ( self.row , self.name )
	
	class Meta:
		verbose_name_plural = u"Cabinets"

class DeviceType( models.Model ):

	name		= models.CharField( max_length = 50 )

	def __str__( self ):
		return "%s" % ( self.name )
	
	class Meta:
		verbose_name_plural = u"Device Types"

class Device( models.Model ):

	type		= models.ForeignKey( DeviceType )
	brand		= models.CharField( max_length = 50 )
	model		= models.CharField( max_length = 50 )
	serial		= models.CharField( max_length = 50 )
	owner		= models.ForeignKey( Company , related_name='owner' )
	manager		= models.ForeignKey( Company , related_name='manager' )
	cabinet		= models.ForeignKey( Cabinet )
	rack_first	= models.SmallIntegerField(default=1)
	rack_last	= models.SmallIntegerField()
	
	def get_absolute_url(self):
		return "/device/" + str(self.id) + "/"

	def __str__( self ):
		return "%s %s %s %s" % ( self.cabinet,  self.type , self.brand , self.model )
	
	class Meta:
		verbose_name_plural = u"Devices"
		ordering = ('-rack_first',)

class PortType( models.Model ):

	name		= models.CharField( max_length = 50 )

	def __str__( self ):
		return "%s" % ( self.name )
	
	class Meta:
		verbose_name_plural = u"Port Types"

class Port( models.Model ):

	type		= models.ForeignKey( PortType )
	device		= models.ForeignKey( Device )
	name		= models.CharField( max_length = 20 )

	def __str__( self ):
		return "%s %s.Port (%s Type)" % ( self.device, self.name , self.type )
	
	class Meta:
		verbose_name_plural = u"Ports"

class Cabling( models.Model ):

	name		= models.CharField( max_length = 50 )
	edge1		= models.ForeignKey( Port , related_name='edge1' )
	edge2		= models.ForeignKey( Port , related_name='edge2' )

	def __str__( self ):
		return "%s %s %s" % ( self.name,  self.edge1 , self.edge2 )
	
	class Meta:
		verbose_name_plural = u"Cablings"
