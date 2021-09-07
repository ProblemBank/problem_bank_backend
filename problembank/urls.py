from problembank.views.accountview import AccountView
from problembank.views.otherviews import add_problem_to_group
from problembank.views.problemview import ProblemView
from problembank.views.problemgroupview import ProblemGroupView
from problembank.views.guidanceview import GuidanceView
from problembank.views.eventview import EventView
from problembank.views.topicsview import TopicView, SubtopicView, SourceView


from django.urls import path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('problem', ProblemView)
router.register('problem/<int:pk>', ProblemView)
router.register('problemgroup', ProblemGroupView)
router.register('problemgroup/<int:pk>', ProblemGroupView)
router.register('guidance', GuidanceView)
router.register('guidance/<int:pk>', GuidanceView)
router.register('event', EventView)
router.register('event/<int:pk>', EventView)
router.register('topic', TopicView)
router.register('topic/<int:pk>', TopicView)
router.register('subtopic', SubtopicView)
router.register('subtopic/<int:pk>', SubtopicView)
router.register('source', SourceView)
router.register('source/<int:pk>', SourceView)
router.register('account', AccountView)
router.register('account/<int:pk>', AccountView)
urlpatterns = [
      path('addproblemtogroup/<int:ppk>/<int:gpk>', add_problem_to_group),
    
]

urlpatterns += router.urls