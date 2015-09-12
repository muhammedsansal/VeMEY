# encoding: utf-8
from django									import forms
from main.models									import *
from django.db								import models
from django.forms							import ModelForm

class CompanyCreateForm(forms.ModelForm):

	class Meta:
		model = Company
		exclude = []
	
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('label_suffix', '')
		super(CompanyCreateForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs.update({'class':'form-control', 'autofocus': 'autofocus'})

class CountryCreateForm(forms.ModelForm):

	class Meta:
		model = Country
		exclude = []
	
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('label_suffix', '')
		super(CountryCreateForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs.update({'class':'form-control', 'autofocus': 'autofocus'})
		self.fields['iso_code'].widget.attrs.update({'class':'form-control', })

class CityCreateForm(forms.ModelForm):

	class Meta:
		model = City
		exclude = ['country']
	
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('label_suffix', '')
		super(CityCreateForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs.update({'class':'form-control', 'autofocus': 'autofocus'})

class BuildingCreateForm(forms.ModelForm):

	class Meta:
		model = Building
		exclude = ['city']
	
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('label_suffix', '')
		super(BuildingCreateForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs.update({'class':'form-control', 'autofocus': 'autofocus'})

class DataCenterRoomCreateForm(forms.ModelForm):

	class Meta:
		model = DataCenterRoom
		exclude = ['building']
	
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('label_suffix', '')
		super(DataCenterRoomCreateForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs.update({'class':'form-control', 'autofocus': 'autofocus'})
		self.fields['square_meter'].widget.attrs.update({'class':'form-control',})
		self.fields['owner'].widget.attrs.update({'class':'form-control',})
		self.fields['manager'].widget.attrs.update({'class':'form-control',})

class RowCreateForm(forms.ModelForm):

	class Meta:
		model = Row
		exclude = ['datacenterroom']
	
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('label_suffix', '')
		super(RowCreateForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs.update({'class':'form-control', 'autofocus': 'autofocus'})

class CabinetCreateForm(forms.ModelForm):

	class Meta:
		model = Cabinet
		exclude = ['row']
	
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('label_suffix', '')
		super(CabinetCreateForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs.update({'class':'form-control', 'autofocus': 'autofocus'})
		self.fields['model'].widget.attrs.update({'class':'form-control', })
		self.fields['owner'].widget.attrs.update({'class':'form-control', })
		self.fields['manager'].widget.attrs.update({'class':'form-control', })
		self.fields['height'].widget.attrs.update({'class':'form-control', })
		self.fields['date'].widget.attrs.update({'class':'form-control', })

class DeviceTypeCreateForm(forms.ModelForm):

	class Meta:
		model = DeviceType
		exclude = []
	
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('label_suffix', '')
		super(DeviceTypeCreateForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs.update({'class':'form-control', 'autofocus': 'autofocus'})

class DeviceCreateForm(forms.ModelForm):

	class Meta:
		model = Device
		exclude = ['cabinet']
	
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('label_suffix', '')
		super(DeviceCreateForm, self).__init__(*args, **kwargs)
		self.fields['type'].widget.attrs.update({'class':'form-control', 'autofocus': 'autofocus'})
		self.fields['manufacturer'].widget.attrs.update({'class':'form-control', })
		self.fields['model'].widget.attrs.update({'class':'form-control', })
		self.fields['serial'].widget.attrs.update({'class':'form-control', })
		self.fields['owner'].widget.attrs.update({'class':'form-control', })
		self.fields['manager'].widget.attrs.update({'class':'form-control', })
		self.fields['rack_first'].widget.attrs.update({'class':'form-control', })
		self.fields['rack_last'].widget.attrs.update({'class':'form-control', })

class PortTypeCreateForm(forms.ModelForm):

	class Meta:
		model = PortType
		exclude = []
	
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('label_suffix', '')
		super(PortTypeCreateForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs.update({'class':'form-control', 'autofocus': 'autofocus'})

class PortCreateForm(forms.ModelForm):

	class Meta:
		model = Port
		exclude = ['device','pair_port']
	
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('label_suffix', '')
		super(PortCreateForm, self).__init__(*args, **kwargs)
		self.fields['type'].widget.attrs.update({'class':'form-control', 'autofocus': 'autofocus'})
		self.fields['name'].widget.attrs.update({'class':'form-control', })
		self.fields['is_paired'].widget.attrs.update({'class':'form-control', })
