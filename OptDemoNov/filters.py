from .models import Truck
import django_filters

class TruckFilter(django_filters.FilterSet):
    class Meta:
        model = Truck
        fields = ['TruckName', 'OwnerName', 'Available']