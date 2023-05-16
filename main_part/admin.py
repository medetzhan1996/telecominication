from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.conf.urls.static import static

admin.site.index_title = _('Telecommunications organization web-site')
admin.site.site_header = _('Telecommunications organization')
admin.site.site_title = _('My Site Management')
from .models import Client, Service, Equipment, Order, Employee
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'address', 'telephone', 'email']
    # list_filter = ['first_name', 'last_name', 'address', 'telephone', 'email']
    # search_fields = ['first_name', 'last_name', 'address', 'telephone', 'email']

admin.site.register(Service)
admin.site.register(Equipment)
admin.site.register(Order)
admin.site.register(Employee)
