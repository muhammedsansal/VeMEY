# encoding: utf-8
from django import forms
from main.models import *
from django.db import models
from django.forms import ModelForm


class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = []

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(CompanyCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'autofocus': 'autofocus'})


class CountryCreateForm(forms.ModelForm):
    class Meta:
        model = Country
        exclude = []

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(CountryCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'autofocus': 'autofocus'})
        self.fields['iso_code'].widget.attrs.update({'class': 'form-control', })


class CityCreateForm(forms.ModelForm):
    class Meta:
        model = City
        exclude = ['country']

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(CityCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'autofocus': 'autofocus'})


class BuildingCreateForm(forms.ModelForm):
    class Meta:
        model = Building
        exclude = ['city']

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(BuildingCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'autofocus': 'autofocus'})


class DataCenterRoomCreateForm(forms.ModelForm):
    class Meta:
        model = DataCenterRoom
        exclude = ['building']

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(DataCenterRoomCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'autofocus': 'autofocus'})
        self.fields['square_meter'].widget.attrs.update({'class': 'form-control', })
        self.fields['owner'].widget.attrs.update({'class': 'form-control', })
        self.fields['manager'].widget.attrs.update({'class': 'form-control', })
        self.fields['customer'].widget.attrs.update({'class': 'form-control', })


class RackCreateForm(forms.ModelForm):
    class Meta:
        model = Rack
        exclude = ['datacenterroom']

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(RackCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'autofocus': 'autofocus'})
        self.fields['model'].widget.attrs.update({'class': 'form-control', })
        self.fields['owner'].widget.attrs.update({'class': 'form-control', })
        self.fields['manager'].widget.attrs.update({'class': 'form-control', })
        self.fields['customer'].widget.attrs.update({'class': 'form-control', })
        self.fields['height'].widget.attrs.update({'class': 'form-control', })
        self.fields['date_installed'].widget.attrs.update({'class': 'form-control', })


class DeviceTypeCreateForm(forms.ModelForm):
    class Meta:
        model = DeviceType
        exclude = []

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(DeviceTypeCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'autofocus': 'autofocus'})


class DeviceCreateForm(forms.ModelForm):
    class Meta:
        model = Device
        exclude = ['rack']

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        # kwargs i??inde gelen 'selected_rack' arg??man??n?? pop ediyoruz.
        # bunu SUPER'den ??nce yapmam??z laz??mm????, ????nk?? SUPER bu arg??man??
        # beklemiyormu??.
        selected_rack = kwargs.pop('selected_rack', None)
        super(DeviceCreateForm, self).__init__(*args, **kwargs)
        # daha ??nce pop etti??imiz 'selected_rack' arg??man??n?? kullanarak RackUnit'leri filtreliyoruz.
        self.fields['rackunit'].queryset = RackUnit.objects.filter(rack=selected_rack)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'autofocus': 'autofocus'})
        self.fields['type'].widget.attrs.update({'class': 'form-control', })
        self.fields['manufacturer'].widget.attrs.update({'class': 'form-control', })
        self.fields['model'].widget.attrs.update({'class': 'form-control', })
        self.fields['serial'].widget.attrs.update({'class': 'form-control', })
        self.fields['owner'].widget.attrs.update({'class': 'form-control', })
        self.fields['manager'].widget.attrs.update({'class': 'form-control', })
        self.fields['customer'].widget.attrs.update({'class': 'form-control', })
        self.fields['rackunit'].widget.attrs.update({'class': 'form-control', })


class PortTypeCreateForm(forms.ModelForm):
    class Meta:
        model = PortType
        exclude = []

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(PortTypeCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'autofocus': 'autofocus'})


class PortCreateForm(forms.ModelForm):
    class Meta:
        model = Port
        exclude = ['device', 'is_paired', 'pair_port']

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(PortCreateForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget.attrs.update({'class': 'form-control', 'autofocus': 'autofocus'})
        self.fields['name'].widget.attrs.update({'class': 'form-control', })


class ConnectionCreateForm(forms.ModelForm):
    class Meta:
        model = Connection
        exclude = ['edge1']

    def  __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(ConnectionCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'autofocus': 'autofocus'})
        #self.fields['edge1'].widget.attrs.update({'class': 'form-control', })
        self.fields['edge2'].widget.attrs.update({'class': 'form-control', })

