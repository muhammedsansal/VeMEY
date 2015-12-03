from django.contrib import admin

# Register your models here.
from main.models import *


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso_code')


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')


class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')


class DataCenterRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'building')


class RowAdmin(admin.ModelAdmin):
    list_display = ('name', 'datacenterroom')


class CabinetAdmin(admin.ModelAdmin):
    list_display = ('name', 'row')


class RackUnitAdmin(admin.ModelAdmin):
    list_display = ('cabinet', 'no')


class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model', 'type', 'serial', 'owner', 'manager', 'cabinet', 'rack_first', 'rack_last')


class PortTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


class PortAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'device')


class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'edge1', 'edge2')


admin.site.register(Company, CompanyAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(DataCenterRoom, DataCenterRoomAdmin)
admin.site.register(Row, RowAdmin)
admin.site.register(Cabinet, CabinetAdmin)
admin.site.register(RackUnit, RackUnitAdmin)
admin.site.register(DeviceType, DeviceTypeAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(PortType, PortTypeAdmin)
admin.site.register(Port, PortAdmin)
admin.site.register(Connection, ConnectionAdmin)
