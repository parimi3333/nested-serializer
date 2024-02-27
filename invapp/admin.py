from django.contrib import admin
from .models import invoice, invoicedetails

# Register your models here.
admin.site.register(invoice)
admin.site.register(invoicedetails)
