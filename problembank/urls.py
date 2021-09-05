from problembank.views.problemview import ProblemView

from django.urls import path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('problem', ProblemView)
router.register('problem/<int:pk>', ProblemView)
urlpatterns = [
     
]

urlpatterns += router.urls