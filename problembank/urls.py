from problembank.views.problemview import ProblemView
from problembank.views.problemgroupview import ProblemGroupView
from problembank.views.eventview import EventView


from django.urls import path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('problem', ProblemView)
router.register('problem/<int:pk>', ProblemView)
router.register('problemgroup', ProblemGroupView)
router.register('problemgroup/<int:pk>', ProblemGroupView)
router.register('event', EventView)
router.register('event/<int:pk>', EventView)
urlpatterns = [
     
]

urlpatterns += router.urls