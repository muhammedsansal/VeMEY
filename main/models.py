# encoding: utf-8

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
        return "%s" % self.name

    class Meta:
        verbose_name_plural = u"Companies"


class Country(models.Model):
    name = models.CharField(max_length=50)
    iso_code = models.CharField(max_length=2)

    def get_absolute_url(self):
        return "/country/" + str(self.id) + "/"

    def __str__(self):
        return "%s" % self.iso_code

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

    def location_string(self):
        return "%s" % self.country.name


class Building(models.Model):
    city = models.ForeignKey(City)
    name = models.CharField(max_length=50)

    def get_absolute_url(self):
        return "/building/" + str(self.id) + "/"

    def __str__(self):
        return "%s - %s" % (self.city, self.name)

    class Meta:
        verbose_name_plural = u"Buildings"

    def location_string(self):
        return "%s, %s" % (self.city.name, self.city.location_string())


class DataCenterRoom(models.Model):
    building = models.ForeignKey(Building)
    name = models.CharField(max_length=50)
    square_meter = models.SmallIntegerField()
    owner = models.ForeignKey(Company, related_name='dc_owner', null=True, blank=True)
    manager = models.ForeignKey(Company, related_name='dc_manager', null=True, blank=True)
    customer = models.ForeignKey(Company, related_name='dc_customer', null=True, blank=True)

    def get_absolute_url(self):
        return "/datacenterroom/" + str(self.id) + "/"

    def __str__(self):
        return "%s - %s" % (self.building.name, self.name)

    class Meta:
        verbose_name_plural = u"Data center rooms"

    def location_string(self):
        return "%s, %s" % (self.building.name, self.building.location_string())


class Rack(models.Model):
    datacenterroom = models.ForeignKey(DataCenterRoom)
    name = models.CharField(max_length=50)
    model = models.CharField(max_length=50, null=True, blank=True)
    owner = models.ForeignKey(Company, related_name='rack_owner', null=True, blank=True)
    manager = models.ForeignKey(Company, related_name='rack_manager', null=True, blank=True)
    customer = models.ForeignKey(Company, related_name='rack_customer', null=True, blank=True)
    height = models.SmallIntegerField(default=42)
    date_installed = models.DateField(default=datetime.date.today, null=True, blank=True)

    def get_absolute_url(self):
        return "/rack/" + str(self.id) + "/"

    def __str__(self):
        return "%s - %s" % (self.datacenterroom, self.name)

    class Meta:
        verbose_name_plural = u"Racks"

    def location_string(self):
        return "%s, %s" % (self.datacenterroom.name, self.datacenterroom.location_string())

    def number_of_empty_rack_units(self):
        empty_racks = 0
        for x in range(1, self.height+1):
            devices = None
            try:
                devices = Device.objects.filter(rack=self, rackunit__no=x)
            except:
                pass

            if not devices:
                empty_racks += 1

        return empty_racks

    def save(self):

        is_new_object = False

        old_height = None

        # nesne daha önce kayıtlı mıymış diye bakıyoruz.
        # böylelikle nesne ilk kez mi yaratılıyor, yoksa
        # update mi ediliyor anlıyoruz.
        try:
            old_obj = Rack.objects.get(pk=self.pk)
            old_height = old_obj.height
        except Rack.DoesNotExist: # yeni nesne
            is_new_object = True
        else:
            is_new_object = False

        # super metodunu burada çağırıyoruz çünkü önce rack'in save edilmesi
        # gerekiyor. rackunit'leri yaratırken bu rack'i kullanacağız.
        # update ediliyorsa sorun değil, update işleminden önceki "height"
        # değerini "old_height"a yazdık.
        super(Rack, self).save()

        # rack ilk kez yaratılıyor. "height" field'ında belirtilen kadar
        # rackunit yaratalım.
        if is_new_object:
            # 42u'luk bir rack ise for döngüsü range(1,43) için işliyor. yani min 1, max 42.
            for x in range(1, self.height+1):
                new_rack_unit = RackUnit(rack=self, no=x)
                new_rack_unit.save()

        # rack update ediliyor.
        else:
            if old_height:
                # eski rack'in rackunit sayısı update ile değiştirilmiş.
                # eksik veya fazla rackunitleri tespit edip düzeltme yapmak
                # lazım. şimdilik "pass" ile geçiştirilsin.
                if old_height != self.height:
                    # rackunit sayısı artırılmış.
                    if old_height < self.height:
                        pass
                    # rackunit sayısı azaltılmış.
                    else:
                        pass


class RackUnit(models.Model):
    rack = models.ForeignKey(Rack)
    no = models.SmallIntegerField(default=0)

    def __str__(self):
        return "%s-%dU" % (self.rack.name, self.no)

    def short_name(self):
        return "%dU" % self.no

    class Meta:
        verbose_name_plural = u"Rack Units"
        ordering = ('-no', )


class DeviceType(models.Model):
    name = models.CharField(max_length=50)
    has_paired_ports = models.BooleanField(default=False)

    def get_absolute_url(self):
        return "/device-type/" + str(self.id) + "/"

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name_plural = u"Device Types"
        ordering = ('name',)


class Device(models.Model):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(DeviceType)
    manufacturer = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    serial = models.CharField(max_length=50)
    owner = models.ForeignKey(Company, related_name='device_owner')
    manager = models.ForeignKey(Company, related_name='device_manager')
    customer = models.ForeignKey(Company, related_name='device_customer', null=True, blank=True)
    rack = models.ForeignKey(Rack)
    rackunit = models.ManyToManyField(RackUnit)

    def get_absolute_url(self):
        return "/device/" + str(self.id) + "/"

    def __str__(self):
        return "%s (%s %s %s)" % (self.name, self.type, self.manufacturer, self.model)

    class Meta:
        verbose_name_plural = u"Devices"
        # ordering rack_first ve rack_last'a göre yapılıyordu.
        # yeni bir ordering belirlemek gerekiyor.
        ordering = ('rack', )

    def location_string(self):
        return "%s, %s" % (self.rack.name, self.rack.location_string())

    def rack_location(self):
        # {x}-{y}U representation of device's location in rack.
        # For a device located in 6,7,8,9 numbered rackunits return value is:
        #   6-9U
        rack_address_list = []
        for rackUnit in reversed(self.rackunit.all()):
            rack_address_list.append(str(rackUnit.no))

        if rack_address_list:
            # return "("+ ','.join(rack_address_list) + ")" + "U"
            return str(rack_address_list[0]) + "-" + str(rack_address_list[-1]) + "U"
        else:
            return ""

    def rack_size(self):
        # Number of rack units device allocates.
        return self.rackunit.all().count()

    def find_ports(self):
        device = self
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
        return "%s" % self.name

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
        while cabling is not None:
            dedicated_cablings.append(cabling)
            if cabling.edge1 == target_port:
                target_port = cabling.edge2
            elif cabling.edge2 == target_port:
                target_port = cabling.edge1
            else:
                pass

            if target_port.is_paired:
                if target_port.pair_port is None:
                    target_port = target_port.pair_port

            cabling = self.get_single_cabling(target_port, dedicated_cablings)

        return dedicated_cablings

    def find_connection_edge(self):
        # start point is self
        target_port = self

        # loop over every cabling connected to each other.
        while True:
            # at every step, a new cabling is found, dedicated to target port.
            connection = Connection.objects.get(Q(edge1=target_port) | Q(edge2=target_port))

            # change 'target_port' variable with the port on the other edge of connection
            if connection.edge1 == target_port:
                target_port = connection.edge2
            elif connection.edge2 == target_port:
                target_port = connection.edge1
            else:
                break

            # if the new target_port has a pair, assign the pair port to 'target_port'
            # so loop will find the next cabling (connection).
            if target_port.is_paired:
                # pair port is not connected. the loop reached its final destination.
                # target_port is the last node of connection. let's break the loop.
                if target_port.pair_port is None:
                    break
                # pair port is assigned to target_port. on the next step, the new cabling
                # will be discovered.
                target_port = target_port.pair_port
            # target port is not a paired port. so we reached the last node. if a port is not
            # paired, the cabling doesnt go on with new connections. it can proceed only to backwards.
            # so lets break the loop. we find the last node.
            else:
                break

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
    if not obj.is_paired:
        if obj.pair_port is not None:
            port = obj.pair_port
            port.delete()
    elif obj.is_paired:
        if obj.pair_port is None:
            new_pair_port = Port(type=obj.type, device=obj.device, name=obj.name + " (pair)", is_paired=True, pair_port=obj)
            new_pair_port.save()
            obj.pair_port = new_pair_port
            obj.save()


class Connection(models.Model):
    name = models.CharField(max_length=50)
    edge1 = models.ForeignKey(Port, related_name='edge1')
    edge2 = models.ForeignKey(Port, related_name='edge2')

    def get_absolute_url(self):
        return "/connection/" + str(self.id) + "/"

    def __str__(self):
        return "%s %s %s" % (self.name, self.edge1, self.edge2)

    class Meta:
        verbose_name_plural = u"Connections"
