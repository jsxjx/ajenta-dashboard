from django.contrib import admin

from .models import Call


class CallAdmin(admin.ModelAdmin):
    list_display = ('callid', 'uniquecallid', 'jointime', 'leavetime')


admin.site.register(Call, CallAdmin)
