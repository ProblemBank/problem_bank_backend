from rest_framework import serializers

from Game.serializers import PlayerSerializer, ProblemSerializer, ProblemInfoSerializer
from .models import *


class AuctionSerializers(serializers.ModelSerializer):
    # problem_id = serializers.IntegerField()
    seller = PlayerSerializer()
    buyer = PlayerSerializer()
    problem = ProblemInfoSerializer()

    class Meta:
        model = Auction
        fields = ['id', 'price', 'seller', 'buyer', 'problem']
        read_only_fields = ['seller', 'buyer', 'problem']
