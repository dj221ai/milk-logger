from django.contrib import admin
from .models import EntryData, RatePerLitre, MonthlyMilkData

admin.site.register(EntryData)
admin.site.register(RatePerLitre)
admin.site.register(MonthlyMilkData)
