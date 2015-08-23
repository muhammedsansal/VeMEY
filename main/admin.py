from django.contrib import admin

# Register your models here.
from main.models import *

admin.site.register( Company )
admin.site.register( Country )
admin.site.register( City )
admin.site.register( Building )
admin.site.register( DataCenterRoom )
admin.site.register( Row )
admin.site.register( Cabinet )
admin.site.register( DeviceType )
admin.site.register( Device )
