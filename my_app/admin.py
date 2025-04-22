from django.contrib import admin

from my_app.models import Table, Dish, Reservation

# Register your models here.
admin.site.register(Table)
admin.site.register(Dish)
admin.site.register(Reservation)
