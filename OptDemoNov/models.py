from django.db import models

# Create your models here.

class SysUsers(models.Model):
    Login = models.CharField(max_length=200)
    Password = models.CharField(max_length=200)
    Name = models.CharField(max_length=200)
    Email = models.CharField(max_length=200)
    AD = 'Admin'
    CA = 'Carrier'
    SH = 'Shipper'
    TYPE_CHOICES = (
        (AD, 'Admin'),
        (CA, 'Carrier'),
        (SH, 'Shipper'),
    )
    Type = models.CharField(
        max_length=7,
        choices=TYPE_CHOICES,
        default=AD,
    )

    def __str__(self):
        return self.Name

class Truck(models.Model):
    TruckName = models.CharField(max_length=200)
    OwnerName = models.ForeignKey(SysUsers, on_delete=models.SET_NULL, null=True, limit_choices_to={'Type':"Carrier"})
    WOT4 = '4WOT'
    WWC4 = '4WWC'
    WRC4 = '4WRC'
    WWC6 = '6WWC'
    WRC6 = '6WRC'
    WC10 = '10WC'
    RC10 = '10RC'
    TRUCK_TYPE_CHOICES = (
    (WOT4, '4 wheel open truck'),
    (WWC4, '4 wheel with cabinet'),
    (WRC4, '4 wheel with refrigerated cabinet'),
    (WWC6, '6 wheel with cabinet'),
    (WRC6, '6 wheel with refrigerated cabinet'),
    (WC10, '10 wheel with cabinet'),
    (RC10, '10 wheel with refrigerated cabinet'),
    )
    TruckType = models.CharField(
        max_length=4,
        choices=TRUCK_TYPE_CHOICES,
        default=WOT4,
    )
    CurrentLon = models.FloatField(default=100.7518861)
    CurrentLat = models.FloatField(default=13.7140519)
    Available = models.BooleanField(default=True)
    TransportationCost = models.FloatField(default=3.0)
    General = models.BooleanField(default=True)
    Perishable = models.BooleanField(default=True)
    Dangerous = models.BooleanField(default=True)
    Valuable = models.BooleanField(default=True)
    Animal = models.BooleanField(default=True)
    DestLon = models.FloatField(default=100.7518861)
    DestLat = models.FloatField(default=13.7140519)


    def __str__(self):
        return self.TruckName