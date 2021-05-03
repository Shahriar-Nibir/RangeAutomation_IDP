import ajax_select
from ajax_select import register, LookupChannel
from .models import *
from django.utils.html import escape


class FirerLookup(LookupChannel):

    model = Firer

    def get_query(self, q, request):
        return Firer.objects.filter(number__icontains=q).order_by('number')

    def get_result(self, obj):
        return obj.number

    def format_match(self, obj):
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        return u"%s" % escape(obj.number)
