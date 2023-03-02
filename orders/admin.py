from django.contrib import admin
from core.admin import admin_site
from  .models import DiscountTicket


class DiscountTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'created_in', 'expired_in', 'value', 'count')
    list_filter = ('id', 'expired_in', 'created_in')
    search_fields = ('id', 'type', 'value', 'expired_in', 'created_in')


# register DiscountTicket
admin_site.register(DiscountTicket, DiscountTicketAdmin)

