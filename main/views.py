from    django.shortcuts import render
from    django.contrib import messages
from    django.http import HttpResponseRedirect, HttpResponse, HttpResponsePermanentRedirect
from    django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from    django.template import RequestContext
from    django.contrib.auth.decorators import login_required, user_passes_test
from    django.contrib.auth import logout
from    django.db.models import Q
from    django.views.generic.edit import CreateView, UpdateView
from    django.contrib.messages.views import SuccessMessageMixin
from    main.models import *
from    main.forms import *


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

    try:
        companies = Company.objects.all()
    except:
        companies = []

    variables = RequestContext(request, {'dcs': dcs, 'companies': companies, })

    return render_to_response('home.html', variables)


class CompanyCreate(CreateView):
    model = Company
    form_class = CompanyCreateForm
    template_name = 'company_create.html'
    success_message = u"Created."


class CompanyUpdate(SuccessMessageMixin, UpdateView):
    model = Company
    form_class = CompanyCreateForm
    template_name = 'company_create.html'
    success_message = u"Updated."


@login_required
def companies(request):
    try:
        companies = Company.objects.all()
    except:
        companies = []

    variables = RequestContext(request, {'companies': companies, })

    return render_to_response('companies.html', variables)


@login_required
def company_detail(request, company_id):
    company = get_object_or_404(Company, id=int(company_id))

    variables = RequestContext(request, {'company': company, })

    return render_to_response('company.html', variables)


@login_required
def countries(request):
    try:
        countries = Country.objects.all()
    except:
        countries = []

    variables = RequestContext(request, {'countries': countries, })

    return render_to_response('countries.html', variables)


@login_required
def country_detail(request, country_id):
    country = get_object_or_404(Country, id=int(country_id))

    try:
        cities = City.objects.filter(country=country)
    except:
        cities = []

    variables = RequestContext(request, {'country': country, 'cities': cities})

    return render_to_response('country.html', variables)


class CountryCreate(CreateView):
    model = Country
    # fields = ['name']
    form_class = CountryCreateForm
    template_name = 'country_create.html'
    success_message = u"Created."


class CountryUpdate(SuccessMessageMixin, UpdateView):
    model = Country
    form_class = CountryCreateForm
    template_name = 'country_create.html'
    success_message = u"Updated."


class CityCreate(SuccessMessageMixin, CreateView):
    model = City
    form_class = CityCreateForm
    template_name = 'city_create.html'
    success_message = u"Created."

    def form_valid(self, form):
        #
        # Sets country field of city
        #
        form.instance.country = get_object_or_404(Country, pk=self.kwargs['country_id'])
        return super(CityCreate, self).form_valid(form)


class CityUpdate(SuccessMessageMixin, UpdateView):
    model = City
    form_class = CityCreateForm
    template_name = 'city_create.html'
    success_message = u"Updated."


@login_required
def city_detail(request, city_id):
    city = get_object_or_404(City, id=int(city_id))

    try:
        buildings = Building.objects.filter(city=city)
    except:
        buildings = []

    variables = RequestContext(request, {'city': city, 'buildings': buildings})

    return render_to_response('city.html', variables)


@login_required
def cities(request):
    try:
        cities = City.objects.all()
    except:
        cities = []

    variables = RequestContext(request, {'cities': cities, })

    return render_to_response('cities.html', variables)


class BuildingCreate(SuccessMessageMixin, CreateView):
    model = Building
    form_class = BuildingCreateForm
    template_name = 'building_create.html'
    success_message = u"Created."

    def form_valid(self, form):
        #
        # Sets country field of city
        #
        form.instance.city = get_object_or_404(City, pk=self.kwargs['city_id'])
        return super(BuildingCreate, self).form_valid(form)


class BuildingUpdate(SuccessMessageMixin, UpdateView):
    model = Building
    form_class = BuildingCreateForm
    template_name = 'building_create.html'
    success_message = u"Updated."


@login_required
def buildings(request):
    try:
        buildings = Building.objects.all()
    except:
        buildings = []

    variables = RequestContext(request, {'buildings': buildings, })

    return render_to_response('buildings.html', variables)


@login_required
def building_detail(request, building_id):
    building = get_object_or_404(Building, id=int(building_id))

    try:
        datacenterrooms = DataCenterRoom.objects.filter(building=building)
    except:
        datacenterrooms = []

    variables = RequestContext(request, {'building': building, 'datacenterrooms': datacenterrooms})

    return render_to_response('building.html', variables)


class DataCenterRoomCreate(SuccessMessageMixin, CreateView):
    model = DataCenterRoom
    form_class = DataCenterRoomCreateForm
    template_name = 'datacenterroom_create.html'
    success_message = u"Created."

    def form_valid(self, form):
        #
        # Sets country field of city
        #
        form.instance.building = get_object_or_404(Building, pk=self.kwargs['building_id'])
        return super(DataCenterRoomCreate, self).form_valid(form)


class DataCenterRoomUpdate(SuccessMessageMixin, UpdateView):
    model = DataCenterRoom
    form_class = DataCenterRoomCreateForm
    template_name = 'datacenterroom_create.html'
    success_message = u"Updated."


@login_required
def datacenterrooms(request):
    try:
        datacenterrooms = DataCenterRoom.objects.all()
    except:
        datacenterrooms = []

    variables = RequestContext(request, {'datacenterrooms': datacenterrooms, })

    return render_to_response('datacenterrooms.html', variables)


@login_required
def data_center_room(request, dc_id):
    data_center_room = get_object_or_404(DataCenterRoom, id=int(dc_id))

    try:
        rows = Row.objects.filter(datacenterroom=data_center_room)

        try:
            cabinets = Cabinet.objects.filter(row__datacenterroom=data_center_room)
        except:
            cabinets = []
    except:
        rows = []

    variables = RequestContext(request, {'data_center_room': data_center_room, 'rows': rows, 'cabinets': cabinets})

    return render_to_response('data_center_room.html', variables)


class RowCreate(SuccessMessageMixin, CreateView):
    model = Row
    form_class = RowCreateForm
    template_name = 'row_create.html'
    success_message = u"Created."

    def form_valid(self, form):
        #
        # Sets country field of city
        #
        form.instance.datacenterroom = get_object_or_404(DataCenterRoom, pk=self.kwargs['dc_id'])
        return super(RowCreate, self).form_valid(form)


class RowUpdate(SuccessMessageMixin, UpdateView):
    model = Row
    form_class = RowCreateForm
    template_name = 'row_create.html'
    success_message = u"Updated."

@login_required
def rows(request):
    try:
        rows = Row.objects.all()
    except:
        rows = []

    variables = RequestContext(request, {'rows': rows, })

    return render_to_response('rows.html', variables)


@login_required
def row(request, row_id):
    row = get_object_or_404(Row, id=int(row_id))

    try:
        cabinets = Cabinet.objects.filter(row=row)
    except:
        cabinets = []

    variables = RequestContext(request, {'row': row, 'cabinets': cabinets})

    return render_to_response('row.html', variables)


class CabinetCreate(SuccessMessageMixin, CreateView):
    model = Cabinet
    form_class = CabinetCreateForm
    template_name = 'cabinet_create.html'
    success_message = u"Created."

    def form_valid(self, form):
        #
        # Sets country field of city
        #
        form.instance.row = get_object_or_404(Row, pk=self.kwargs['row_id'])
        return super(CabinetCreate, self).form_valid(form)


class CabinetUpdate(SuccessMessageMixin, UpdateView):
    model = Cabinet
    form_class = CabinetCreateForm
    template_name = 'cabinet_create.html'
    success_message = u"Updated."

@login_required
def cabinets(request):
    try:
        cabinets = Cabinet.objects.all()
    except:
        cabinets = []

    variables = RequestContext(request, {'cabinets': cabinets, })

    return render_to_response('cabinets.html', variables)


@login_required
def cabinet(request, cabinet_id):
    cabinet = get_object_or_404(Cabinet, id=int(cabinet_id))

    try:
        devices = Device.objects.filter(cabinet=cabinet)
    except:
        devices = []

    variables = RequestContext(request, {'cabinet': cabinet, 'devices': devices})

    return render_to_response('cabinet.html', variables)


@login_required
def device_types(request):
    try:
        device_types = DeviceType.objects.all()
    except:
        device_types = []

    variables = RequestContext(request, {'device_types': device_types, })

    return render_to_response('device_types.html', variables)


class DeviceTypeCreate(SuccessMessageMixin, CreateView):
    model = DeviceType
    form_class = DeviceTypeCreateForm
    template_name = 'device_type_create.html'
    success_message = u"Created."


class DeviceTypeUpdate(SuccessMessageMixin, UpdateView):
    model = DeviceType
    form_class = DeviceTypeCreateForm
    template_name = 'device_type_create.html'
    success_message = u"Updated."


@login_required
def device_type(request, device_type_id):
    device_type = get_object_or_404(DeviceType, id=int(device_type_id))

    variables = RequestContext(request, {'device_type': device_type, })

    return render_to_response('device_type.html', variables)


@login_required
def device(request, device_id):
    device = get_object_or_404(Device, id=int(device_id))

    try:
        reserved_ports = Port.objects.filter(Q(device=device), Q(edge1__isnull=False) | Q(edge2__isnull=False))
    except:
        reserved_ports = []

    try:
        unreserved_ports = Port.objects.filter(Q(device=device), Q(edge1__isnull=True) & Q(edge2__isnull=True))
    except:
        unreserved_ports = []

    variables = RequestContext(request, {'device': device, 'reserved_ports': reserved_ports,
                                         'unreserved_ports': unreserved_ports})

    return render_to_response('device.html', variables)


@login_required
def devices(request):
    try:
        devices = Device.objects.all()
    except:
        devices = []

    variables = RequestContext(request, {'devices': devices, })

    return render_to_response('devices.html', variables)


class DeviceCreate(SuccessMessageMixin, CreateView):
    model = Device
    form_class = DeviceCreateForm
    template_name = 'device_create.html'
    success_message = u"Created."

    def form_valid(self, form):
        #
        # Sets country field of city
        #
        form.instance.cabinet = get_object_or_404(Cabinet, pk=self.kwargs['cabinet_id'])
        return super(DeviceCreate, self).form_valid(form)

class DeviceUpdate(SuccessMessageMixin, UpdateView):
    model = Device
    form_class = DeviceCreateForm
    template_name = 'device_create.html'
    success_message = u"Updated."


@login_required
def port_types(request):
    try:
        port_types = PortType.objects.all()
    except:
        port_types = []

    variables = RequestContext(request, {'port_types': port_types, })

    return render_to_response('port_types.html', variables)


class PortTypeCreate(SuccessMessageMixin, CreateView):
    model = PortType
    form_class = PortTypeCreateForm
    template_name = 'port_type_create.html'
    success_message = u"Created."


class PortTypeUpdate(SuccessMessageMixin, UpdateView):
    model = PortType
    form_class = PortTypeCreateForm
    template_name = 'port_type_create.html'
    success_message = u"Updated."


@login_required
def port_type(request, port_type_id):
    port_type = get_object_or_404(PortType, id=int(port_type_id))

    variables = RequestContext(request, {'port_type': port_type, })

    return render_to_response('port_type.html', variables)


@login_required
def port(request, port_id):
    port = get_object_or_404(Port, id=int(port_id))

    connections = port.find_connections()

    variables = RequestContext(request, {'port': port, 'connections': connections})

    return render_to_response('port.html', variables)


class PortCreate(SuccessMessageMixin, CreateView):
    model = Port
    form_class = PortCreateForm
    template_name = 'port_create.html'
    success_message = u"Created."

    def form_valid(self, form):
        #
        # Sets country field of city
        #
        form.instance.device = get_object_or_404(Device, pk=self.kwargs['device_id'])
        return super(PortCreate, self).form_valid(form)

class PortUpdate(SuccessMessageMixin, UpdateView):
    model = Port
    form_class = PortCreateForm
    template_name = 'port_create.html'
    success_message = u"Updated."

@login_required
def ports(request):
    try:
        ports = Port.objects.all()
    except:
        ports = []

    variables = RequestContext(request, {'ports': ports, })

    return render_to_response('ports.html', variables)


@login_required
def connections(request):
    try:
        connections = Connection.objects.all()
    except:
        connections = []

    variables = RequestContext(request, {'connections': connections, })

    return render_to_response('connections.html', variables)


@login_required
def connection(request, connection_id):
    connection = get_object_or_404(Connection, id=int(connection_id))

    variables = RequestContext(request, {'connection': connection, })   # burası kontrol edilmeli

    return render_to_response('connection.html', variables)


class ConnectionCreate(SuccessMessageMixin, CreateView):
    model = Connection
    form_class = ConnectionCreateForm
    template_name = 'connection_create.html'
    success_message = u"Created."

    def form_valid(self, form):
        #
        # Sets country field of city
        #
        form.instance.edge1 = get_object_or_404(Port, pk=self.kwargs['port_id'])
        return super(ConnectionCreate, self).form_valid(form)