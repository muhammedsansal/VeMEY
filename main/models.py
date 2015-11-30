from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.db.models import Q
import datetime


# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=50)

    def get_absolute_url(self):
        return "/company/" + str(self.id) + "/"

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name_plural = u"Companies"


class Country(models.Model):
    name = models.CharField(max_length=50)
    iso_code = models.CharField(max_length=2)

    def get_absolute_url(self):
        return "/country/" + str(self.id) + "/"

    def __str__(self):
        return "%s" % (self.iso_code)

    class Meta:
        verbose_name_plural = u"Countries"


class City(models.Model):
    country = models.ForeignKey(Country)
    name = models.CharField(max_length=50)

    def get_absolute_url(self):
        return "/city/" + str(self.id) + "/"

    def __str__(self):
        return "%s - %s" % (self.country.iso_code, self.name)

    class Meta:
        verbose_name_plural = u"Cities"


class Building(models.Model):
    city = models.ForeignKey(City)
    name = models.CharField(max_length=50)

    def get_absolute_url(self):
        return "/building/" + str(self.id) + "/"

    def __str__(self):
        return "%s - %s" % (self.city, self.name)

    class Meta:
        verbose_name_plural = u"Buildings"


class DataCenterRoom(models.Model):
    building = models.ForeignKey(Building)
    name = models.CharField(max_length=50)
    square_meter = models.SmallIntegerField()
    owner = models.ForeignKey(Company, related_name='dc_owner', null=True, blank=True)
    manager = models.ForeignKey(Company, related_name='dc_manager', null=True, blank=True)

    def get_absolute_url(self):
        return "/datacenterroom/" + str(self.id) + "/"

    def __str__(self):
        return "%s - %s" % (self.building, self.name)

    class Meta:
        verbose_name_plural = u"Data center rooms"


class Row(models.Model):
    datacenterroom = models.ForeignKey(DataCenterRoom)
    name = models.CharField(max_length=50)

    def get_absolute_url(self):
        return "/row/" + str(self.id) + "/"

    def __str__(self):
        return "%s - %s" % (self.datacenterroom, self.name)

    class Meta:
        verbose_name_plural = u"Rows"


class Cabinet(models.Model):
    row = models.ForeignKey(Row)
    name = models.CharField(max_length=50)
    model = models.CharField(max_length=50, null=True, blank=True)
    owner = models.ForeignKey(Company, related_name='cabinet_owner', null=True, blank=True)
    manager = models.ForeignKey(Company, related_name='cabinet_manager', null=True, blank=True)
    height = models.SmallIntegerField(default=42)
    date = models.DateField(default=datetime.date.today, null=True, blank=True)

    def get_absolute_url(self):
        return "/cabinet/" + str(self.id) + "/"

    def __str__(self):
        return "%s - %s" % (self.row, self.name)

    class Meta:
        verbose_name_plural = u"Cabinets"


class DeviceType(models.Model):
    name = models.CharField(max_length=50)

    def get_absolute_url(self):
        return "/device-type/" + str(self.id) + "/"

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name_plural = u"Device Types"


class Device(models.Model):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(DeviceType)
    manufacturer = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    serial = models.CharField(max_length=50)
    owner = models.ForeignKey(Company, related_name='device_owner')
    manager = models.ForeignKey(Company, related_name='device_manager')
    cabinet = models.ForeignKey(Cabinet)
    rack_first = models.SmallIntegerField(default=1)
    rack_last = models.SmallIntegerField()

    def get_absolute_url(self):
        return "/device/" + str(self.id) + "/"

    def __str__(self):
        return "%s %s %s %s" % (self.cabinet, self.type, self.manufacturer, self.model)

    class Meta:
        verbose_name_plural = u"Devices"
        ordering = ('-rack_first',)

    def find_ports(self):
        device=self
        try:
            my_ports = list(Port.objects.filter(Q(device=device)))
        except:
            my_ports = []
        return my_ports

    def find_reserved_ports(self):
        pass

    def find_unreserved_ports(self):
        pass


class PortType(models.Model):
    name = models.CharField(max_length=50)

    def get_absolute_url(self):
        return "/port-type/" + str(self.id) + "/"

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name_plural = u"Port Types"


class Port(models.Model):
    type = models.ForeignKey(PortType)
    device = models.ForeignKey(Device)
    name = models.CharField(max_length=20)
    is_paired = models.BooleanField(default=False)
    pair_port = models.ForeignKey('self', null=True, blank=True, editable=False, on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return "/port/" + str(self.id) + "/"

    def __str__(self):
        return "%s %s.Port (%s Type)" % (self.device, self.name, self.type)

    class Meta:
        verbose_name_plural = u"Ports"

    def find_connections(self):
        dedicated_cablings = []
        target_port = self
        cabling = self.get_single_cabling(target_port, dedicated_cablings)
        while (cabling != None):
            dedicated_cablings.append(cabling)
            if cabling.edge1 == target_port:
                target_port = cabling.edge2
            elif cabling.edge2 == target_port:
                target_port = cabling.edge1
            else:
                pass

            if target_port.is_paired == True:
                if target_port.pair_port != None:
                    target_port = target_port.pair_port

            cabling = self.get_single_cabling(target_port, dedicated_cablings)

        return dedicated_cablings

    def find_connection_edge(self):
        dedicated_cablings = []
        target_port = self
        cabling = self.get_single_cabling(target_port, dedicated_cablings)
        while (cabling != None):
            dedicated_cablings.append(cabling)
            if cabling.edge1 == target_port:
                target_port = cabling.edge2
            elif cabling.edge2 == target_port:
                target_port = cabling.edge1
            else:
                pass

            if target_port.is_paired == True:
                if target_port.pair_port != None:
                    target_port = target_port.pair_port

            cabling = self.get_single_cabling(target_port, dedicated_cablings)

        return target_port

    def get_single_cabling(self, port, dedicated_cablings):
        try:
            all_filtered_cablings = list(Connection.objects.filter(Q(edge1=port) | Q(edge2=port)))
        except:
            all_filtered_cablings = []

        for cabling in all_filtered_cablings:
            if dedicated_cablings.count(cabling) == 0:
                return cabling
            else:
                return None


@receiver(post_save, sender=Port)
def port_post_save(sender, **kwargs):
    # the object which is deleted can be accessed via kwargs 'instance' key.
    obj = kwargs['instance']
    if (obj.is_paired == False):
        if (obj.pair_port != None):
            port = obj.pair_port
            port.delete()
    elif (obj.is_paired == True):
        if (obj.pair_port == None):
            new_pair_port = Port(type=obj.type, device=obj.device, name=obj.name + " (pair)", is_paired=True,
                                 pair_port=obj)
            new_pair_port.save()
            obj.pair_port = new_pair_port
            obj.save()


class Connection(models.Model):
    name = models.CharField(max_length=50)
    edge1 = models.ForeignKey(Port)
    edge2 = models.ForeignKey(Port, related_name='edge2')

    def get_absolute_url(self):
        return "/connection/" + str(self.id) + "/"

    def __str__(self):
        return "%s %s %s" % (self.name, self.edge1, self.edge2)

    class Meta:
        verbose_name_plural = u"Connections"
