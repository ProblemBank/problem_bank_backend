from problembank.serializers import AutoCheckSubmitSerializer
from problembank.views.accountview import AccountView
from problembank.views.otherviews import add_problem_to_group, remove_problem_from_group, get_event
from problembank.views.problemview import ProblemView, get_all_problems, copy_problem_to_group
from problembank.views.problemgroupview import ProblemGroupView
from problembank.views.guidanceview import GuidanceView
from problembank.views.eventview import EventView
from problembank.views.topicsview import TopicView, SubtopicView, SourceView
from problembank.views.submitview import AutoCheckSubmitView, JudgeableSubmitView
from problembank.views.submitview import  submit_answer_to_problem, judge_answer_view, get_judgeable_submits
from problembank.views.filterview import get_problem_by_filter_view


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
router.register('jugeablesubmit', JudgeableSubmitView)
router.register('jugeablesubmit/<int:pk>', JudgeableSubmitView)
router.register('autochecksubmit', AutoCheckSubmitView)
router.register('autochecksubmit/<int:pk>', AutoCheckSubmitView)
urlpatterns = [
      path('addproblemtogroup/<int:pid>/<int:gid>/', add_problem_to_group),
      path('removeproblemfromgroup/<int:pid>/<int:gid>/', remove_problem_from_group),
      path('getallproblems/', get_all_problems),
      path('getproblembyfilter/', get_problem_by_filter_view),
      path('copyproblemtogroup/<int:pid>/<int:gid>/', copy_problem_to_group),
      path('submit/<int:pid>/<int:gid>/', submit_answer_to_problem),
      path('judge/<int:pk>/<int:mark>/', judge_answer_view),
      path('getsubmits/', get_judgeable_submits),
      path('getevent/<int:pk>/', get_event),
]

urlpatterns += router.urls