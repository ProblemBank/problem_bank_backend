from rest_framework import serializers
from .models import *


class AuctionSerializers(serializers.ModelSerializer):
    # problem_id = serializers.IntegerField()

    class Meta:
        model = Auction
        fields = ['title', 'price']