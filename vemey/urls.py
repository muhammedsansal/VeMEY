"""vemey URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from main.views			import *
from django.contrib.auth import views as auth_views

urlpatterns = [
	url(r'^accounts/login/$', auth_views.login),
	url(r'^logout/$'		, logout_page),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^$', home),
	
	url(r'^company/$'								, companies),
	url(r'^company/add/$'							, CompanyCreate.as_view(),name='company_create'),
	url(r'^company/(?P<company_id>\d+)/$'					, company_detail),
	
	url(r'^country/$'								, countries),
	url(r'^country/add/$'							, CountryCreate.as_view(),name='country_create'),
	url(r'^country/(?P<country_id>\d+)/$'			, country_detail),
	url(r'^country/(?P<pk>\d+)/update/$'			, CountryUpdate.as_view(),name='country_update'),
	url(r'^country/(?P<country_id>\d+)/city/add/$'	, CityCreate.as_view(),name='city_create'),
	
	url(r'^city/(?P<city_id>\d+)/$'					, city_detail),
	url(r'^city/$'					, cities),
	url(r'^city/(?P<city_id>\d+)/building/add/$'	, BuildingCreate.as_view(),name='building_create'),
	
	url(r'^building/(?P<building_id>\d+)/$'					, building_detail),
	url(r'^building/$'					, buildings),
	url(r'^building/(?P<building_id>\d+)/datacenterroom/add/$'	, DataCenterRoomCreate.as_view(),name='datacenterroom_create'),
	
	url(r'^datacenterroom/(?P<dc_id>\d+)/$'								, data_center_room),
	url(r'^datacenterroom/$'					, datacenterrooms),
	url(r'^datacenterroom/(?P<dc_id>\d+)/row/add/$'				, RowCreate.as_view(),name='row_create'),
	
	url(r'^row/(?P<row_id>\d+)/$'								, row),
	url(r'^row/$'					, rows),
	url(r'^row/(?P<row_id>\d+)/cabinet/add/$'			, CabinetCreate.as_view(),name='cabinet_create'),
	
	url(r'^cabinet/(?P<cabinet_id>\d+)/$'								, cabinet),
	url(r'^cabinet/$'					, cabinets),
	url(r'^cabinet/(?P<cabinet_id>\d+)/device/add/$'			, DeviceCreate.as_view(),name='device_create'),
	
	url(r'^device-type/$'								, device_types),
	url(r'^device-type/add/$'							, DeviceTypeCreate.as_view(),name='device_type_create'),
	url(r'^device-type/(?P<device_type_id>\d+)/$'								, device_type),
	
	url(r'^device/(?P<device_id>\d+)/$'								, device),
	url(r'^device/$'					, devices),
	url(r'^device/(?P<device_id>\d+)/port/add/$'			, PortCreate.as_view(),name='port_create'),
	
	url(r'^port-type/$'								, port_types),
	url(r'^port-type/add/$'							, PortTypeCreate.as_view(),name='port_type_create'),
	url(r'^port-type/(?P<port_type_id>\d+)/$'								, port_type),
	
	url(r'^port/(?P<port_id>\d+)/$'								, port),
	url(r'^port/$'								, ports),
	
	url(r'^connection/$'								, connections),
	url(r'^connection/(?P<connection_id>\d+)/$'								, connection),
]
