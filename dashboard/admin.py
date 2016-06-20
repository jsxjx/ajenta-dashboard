from django.contrib import admin

from .models import Call


# Add in this class to customized the Admin Interface
class CallAdmin(admin.ModelAdmin):
    list_display = ('callid', 'uniquecallid', 'jointime', 'leavetime')


admin.site.register(Call, CallAdmin)
