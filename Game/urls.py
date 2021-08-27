from django.urls import path
from .views import *

app_name = 'Account'
urlpatterns = [
    path('<int:game_id>/player/', PlayerView.as_view(), name='get player info'),
    path('<int:game_id>/subject/', SubjectView.as_view(), name='subjects'),
    path('<int:game_id>/problem/', ProblemView.as_view(), name='get all player problems'),
    path('<int:game_id>/problem/scoreboard/', ScoreboardView.as_view(), name='get all player problems'),
    path('<int:game_id>/problem/<int:problem_id>/',
         PlayerSingleProblemView.as_view(), name='one detailed problem'),
    path('<int:game_id>/mentor/problem/', GetAnswerForCorrectionView.as_view(), name='problem correction'),
    path('<int:game_id>/mentor/problem/<int:answer_id>/', MarkAnswerView.as_view(), name='problem correction'),
    path('<int:game_id>/mentor/problem/add/', AddProblemView.as_view(),
         name='problem correction'),

    # path('<int:game_id>/problem/multiple/', MultipleProblemView.as_view(), name='one problem'),
    # path('<int:game_id>/problem/multiple/<int:problem_id>/',
    #      PlayerMultipleProblemView.as_view(), name='one problem'),
    # path('<int:game_id>/hint/<int:problem_id>/',
    #      HintView.as_view(), name='hint of problem'),
    # path('mentor/hint/', HintAnswering.as_view(), name='answer hint'),
]
