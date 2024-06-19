from rest_framework import serializers

from .models import Task,User
from geopy.geocoders import Nominatim

# User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile_number', 'address', 'latitude', 'longitude', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            mobile_number=validated_data['mobile_number'],
            address=validated_data['address'],
        )
        user.set_password(validated_data['password'])
        self.update_address_lat_long(user)
        user.save()
        return user

    def update_address_lat_long(self, user):
        geolocator = Nominatim(user_agent="task_manager")
        location = geolocator.geocode(user.address)
        if location:
            user.latitude = location.latitude
            user.longitude = location.longitude
        else:
            raise serializers.ValidationError("Address could not be geocoded.")

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'date_time', 'assigned_to', 'status']
