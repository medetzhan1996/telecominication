from django.contrib import admin
from django.urls import path, include
from django_otp.admin import OTPAdminSite

from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_text
from django.utils import timezone
from django.db.models import Q

class DateRangeFilter(admin.SimpleListFilter):
    title = _('Date range')
    parameter_name = 'date_range'

    def lookups(self, request, model_admin):
        return (
            ('today', _('Today')),
            ('yesterday', _('Yesterday')),
            ('this_week', _('This week')),
            ('last_week', _('Last week')),
            ('this_month', _('This month')),
            ('last_month', _('Last month')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'today':
            start_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)
            return queryset.filter(date__range=(start_date, end_date))
        if self.value() == 'yesterday':
            start_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0) - timezone.timedelta(days=1)
            end_date = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999) - timezone.timedelta(days=1)
            return queryset.filter(date__range=(start_date, end_date))
        if self.value() == 'this_week':
            start_date = timezone.now().date() - timezone.timedelta(days=timezone.now().weekday())
            end_date = start_date + timezone.timedelta(days=6)
            return queryset.filter(date__range=(start_date, end_date))
        if self.value() == 'last_week':
            start_date = timezone.now().date() - timezone.timedelta(days=timezone.now().weekday() + 7)
            end_date = start_date + timezone.timedelta(days=6)
            return queryset.filter(date__range=(start_date, end_date))
        if self.value() == 'this_month':
            start_date = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timezone.timedelta(days=timezone.now().date().day, hours=23, minutes=59, seconds=59, microseconds=999999)
            return queryset.filter(date__range=(start_date, end_date))
        if self.value() == 'last_month':
            start_date = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timezone.timedelta(days=1)
            end_date = start_date.replace(day=start_date.date().day) + timezone.timedelta(days=timezone.now().date().day, hours=23, minutes=59, seconds=59, microseconds=999999)
            return queryset.filter(date__range=(start_date, end_date))

from django.conf import settings
class OTPAdmin(OTPAdminSite):
    pass
admin_site = OTPAdmin(name="OTPAdmin")


from django.contrib.auth.models import User
from main_part.models import Client, Service, Equipment, Order, Employee, TechnicalSupport
from django_otp.plugins.otp_totp.models import TOTPDevice


class ClientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'address', 'telephone', 'email']
    search_fields = ['first_name', 'last_name', 'address', 'telephone', 'email']
admin_site.register(Client, ClientAdmin)

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
class UserAdmin(BaseUserAdmin):
    search_fields = ('username', 'email')
    search_help_text = 'Enter username or email'
admin_site.register(User, UserAdmin)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['cost_per_month', 'service_type', 'equipment']
    list_filter = ['service_type']
admin_site.register(Service, ServiceAdmin)

class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'processor', 'ram', 'disk_array', 'nic', 'video_card', 'operation_system',
                    'processor_clock', 'total_phisical_memory', 'ram_size']
admin_site.register(Equipment, EquipmentAdmin)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'position']
    search_fields = ['first_name', 'last_name']
    list_filter = ['position']
admin_site.register(Employee, EmployeeAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['client', 'service', 'employee', 'date_start', 'date_end', 'status']
    search_fields = ['client__first_name', 'client__last_name']
    list_filter = ['service', 'status']
admin_site.register(Order, OrderAdmin)

class TechnicalSupportAdmin(admin.ModelAdmin):
    list_display = ['client', 'date', 'description', 'status']
    search_fields = ['client__first_name', 'client__last_name', 'description']
    list_filter = ['status', DateRangeFilter]
admin_site.register(TechnicalSupport, TechnicalSupportAdmin)
import urllib.parse
from django.urls import reverse

import base64
from django.utils.html import format_html
import qrcode
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image


class TOTPDeviceAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'confirmed', 'display_qrcode']
    search_fields = ['user__username', 'name']
    search_help_text = "Search TOTP devices by user's username or name"

    def display_qrcode(self, obj):
        print()
        secret_key = base64.b32encode(obj.bin_key).decode()
        otpauth_url = f'otpauth://totp/{urllib.parse.quote(obj.name)}?secret={secret_key}&algorithm=SHA1&digits=6&period=30'

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=0,
        )
        qr.add_data(otpauth_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        return format_html(f'<img src="data:image/jpeg;base64,{img_str}" alt="QR Code" />')
    display_qrcode.short_description = 'QR Code'


admin_site.register(TOTPDevice, TOTPDeviceAdmin)

urlpatterns = [
    path('admin/', admin_site.urls,),
    path('dadmin/', admin.site.urls),

]

if not settings.DEBUG:
    admin.site.__class__ = OTPAdminSite
    admin_site.__class__ = OTPAdminSite
