from django.db import models

# Create your models here.

class Company( models.Model ):

	name		= models.CharField( max_length = 50 )

	def __unicode__( self ):
		return u"%s" % ( smart_unicode(self.iso_code))
	
	class Meta:
		verbose_name_plural = u"Companies"

class Country( models.Model ):

	name		= models.CharField( max_length = 50 )
	iso_code	= models.CharField( max_length = 2 )

	def __unicode__( self ):
		return u"%s" % ( smart_unicode(self.iso_code))
	
	class Meta:
		verbose_name_plural = u"Countries"

class City( models.Model ):

	name		= models.CharField( max_length = 50 )

	def __unicode__( self ):
		return u"%s" % ( smart_unicode(self.name))
	
	class Meta:
		verbose_name_plural = u"Cities"

class Building( models.Model ):

	name		= models.CharField( max_length = 50 )

	def __unicode__( self ):
		return u"%s" % ( smart_unicode(self.name))
	
	class Meta:
		verbose_name_plural = u"Buildings"

class DataCenterRoom( models.Model ):

	name		= models.CharField( max_length = 50 )

	def __unicode__( self ):
		return u"%s" % ( smart_unicode(self.name))
	
	class Meta:
		verbose_name_plural = u"Data center rooms"

class Row( models.Model ):

	name		= models.CharField( max_length = 50 )

	def __unicode__( self ):
		return u"%s" % ( smart_unicode(self.name))
	
	class Meta:
		verbose_name_plural = u"Rows"

class Cabinet( models.Model ):

	name		= models.CharField( max_length = 50 )

	def __unicode__( self ):
		return u"%s" % ( smart_unicode(self.name))
	
	class Meta:
		verbose_name_plural = u"Cabinets"

class DeviceType( models.Model ):

	name		= models.CharField( max_length = 50 )

	def __unicode__( self ):
		return u"%s" % ( smart_unicode(self.name))
	
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
	rack		= models.SmallIntegerField()

	def __unicode__( self ):
		return u"%s" % ( smart_unicode(self.name))
	
	class Meta:
		verbose_name_plural = u"Devices"
