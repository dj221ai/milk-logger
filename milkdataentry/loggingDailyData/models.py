from decimal import Decimal

from django.conf import settings
from django.db import models
import datetime


class EntryData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today, verbose_name="Date")
    daily_intake = models.FloatField(default=0.0, verbose_name="Daily Milk Intake")
    extra_intake = models.FloatField(default=0.0, verbose_name="Extra Milk Intake", blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.extra_intake is None:
            self.extra_intake = Decimal(0.0)
        super(EntryData, self).save(*args, **kwargs)


class RatePerLitre(models.Model):
    rate_per_litre = models.FloatField(default=1.0, verbose_name="Rate Per Litre")

    def __unicode__(self):
        return self.rate_per_litre


class MonthlyMilkData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_monthly_milk = models.FloatField(default=0.0, verbose_name="Total Monthly Milk Data")