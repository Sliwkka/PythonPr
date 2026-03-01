from django.contrib import admin
from reservations.models import Car, Brand, Model, Reservation


# Register your models here.
class ModelAdmin(admin.ModelAdmin):
    fields = ["brand", "name", "generation", "segment", "description"]


class CarAdmin(admin.ModelAdmin):
    list_display = ["model", "plate_number", "is_reserved"]
    readonly_fields = ["is_reserved"]


admin.site.register(Car, CarAdmin)
admin.site.register(Brand)
admin.site.register(Model, ModelAdmin)
admin.site.register(Reservation)