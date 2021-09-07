from problembank.views.problemview import ProblemView
from problembank.views.problemgroupview import ProblemGroupView


from django.urls import path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('problem', ProblemView)
router.register('problem/<int:pk>', ProblemView)
router.register('ProblemGroup', ProblemGroupView)
router.register('ProblemGroup/<int:pk>', ProblemGroupView)
urlpatterns = [
     
]

urlpatterns += router.urls