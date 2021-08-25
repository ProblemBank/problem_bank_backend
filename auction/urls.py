from django.urls import path
from .views import *

app_name = 'auction'
urlpatterns = [
    path('create/', CreateAuctionProblem.as_view(), name='create-auction'),
    path('<int:game_id>/', AllAuctionsView.as_view(), name='buy-auction'),
    path('<int:game_id>/buy/', BuyAuctionProblem.as_view(), name='buy-auction'),
]
