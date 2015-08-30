from django.shortcuts import render
from	django.contrib					import	messages
from	django.http						import	HttpResponseRedirect, HttpResponse, HttpResponsePermanentRedirect
from	django.shortcuts				import	render_to_response, get_object_or_404, get_list_or_404
from	django.template					import	RequestContext
from	django.contrib.auth.decorators	import	login_required, user_passes_test
from	django.contrib.auth				import	logout
from	django.db.models				import	Q
from	main.models			import *

@login_required
def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')

@login_required
def home(request):

	try:
		dcs = DataCenterRoom.objects.all()
	except:
		dcs = []
		
	variables = RequestContext( request , {'dcs':dcs,} )

	return render_to_response('home.html' , variables )

@login_required
def data_center_room(request,dc_id):

	data_center_room = get_object_or_404(DataCenterRoom,id=int(dc_id))
	
	try:
		rows = Row.objects.filter(datacenterroom=data_center_room)
		
		try:
			cabinets = Cabinet.objects.filter(row__datacenterroom=data_center_room)
		except:
			cabinets = []
	except:
		rows = []
		
	variables = RequestContext( request , {'data_center_room':data_center_room,'rows':rows,'cabinets':cabinets} )

	return render_to_response('data_center_room.html' , variables )

@login_required
def row(request,row_id):

	row = get_object_or_404(Row,id=int(row_id))

	try:
		cabinets = Cabinet.objects.filter(row=row)
	except:
		cabinets = []
		
	variables = RequestContext( request , {'row':row,'cabinets':cabinets} )

	return render_to_response('row.html' , variables )

@login_required
def cabinet(request,cabinet_id):

	cabinet = get_object_or_404(Cabinet,id=int(cabinet_id))
	
	try:
		devices = Device.objects.filter(cabinet=cabinet)
	except:
		devices = []
	
	
		
	variables = RequestContext( request , {'cabinet':cabinet,'devices':devices} )

	return render_to_response('cabinet.html' , variables )
	
@login_required
def device(request,device_id):

	device = get_object_or_404(Device,id=int(device_id))
	
	try:
		reserved_ports = Port.objects.filter(Q(device=device),Q(edge1__isnull=False) | Q(edge2__isnull=False))
	except:
		reserved_ports = []
	
	try:
		nonreserved_ports = Port.objects.filter(Q(device=device),Q(edge1__isnull=True) & Q(edge2__isnull=True))
	except:
		nonreserved_ports = []
		
	variables = RequestContext( request , {'device':device,'reserved_ports':reserved_ports,'nonreserved_ports':nonreserved_ports} )

	return render_to_response('device.html' , variables )
