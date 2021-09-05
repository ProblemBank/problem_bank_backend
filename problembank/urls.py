from problembank.views.problemview import ProblemView
from problembank.views.problemcategoryview import ProblemCategoryView


from django.urls import path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('problem', ProblemView)
router.register('problem/<int:pk>', ProblemView)
router.register('problemcategory', ProblemCategoryView)
router.register('problemcategory/<int:pk>', ProblemCategoryView)
urlpatterns = [
     
]

urlpatterns += router.urls