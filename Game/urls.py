from django.urls import path

from Game.view.exchange import get_all_exchanges, ExchangeView
from Game.view.account import *
from Game.view.submitview import *
urlpatterns = [
    path('notification/', NotificationView.as_view(), name='user notifications'),
    path('player/', PlayerView.as_view(), name='get player info'),

    path('scoreboard/', ScoreboardView.as_view(), name='get scoreboard'),

    path('exchange/all/', get_all_exchanges, name='get all exchanges'),
    path('exchange/', ExchangeView.as_view(), name='player exchange'),

    path('getproblemfromgroup/<int:gid>/', get_problem_from_group),
    path('submitanswer/', submit_answer),
    path('judge/<int:sid>/<int:mark>/', judge),
    # path('<int:game_id>/subject/', SubjectView.as_view(), name='subjects'),
    # path('<int:game_id>/problem/', ProblemView.as_view(), name='get all player problems'),
    # path('<int:game_id>/problem/<int:problem_id>/',
    #      PlayerSingleProblemView.as_view(), name='one detailed problem'),
    # path('<int:game_id>/mentor/problem/', GetAnswerForCorrectionView.as_view(), name='problem correction'),
    # path('<int:game_id>/mentor/problem/<int:answer_id>/', MarkAnswerView.as_view(), name='problem correction'),
    # path('<int:game_id>/mentor/problem/add/', AddProblemView.as_view(),
    #      name='problem correction'),

    # path('<int:game_id>/problem/multiple/', MultipleProblemView.as_view(), name='one problem'),
    # path('<int:game_id>/problem/multiple/<int:problem_id>/',
    #      PlayerMultipleProblemView.as_view(), name='one problem'),
    # path('<int:game_id>/hint/<int:problem_id>/',
    #      HintView.as_view(), name='hint of problem'),
    # path('mentor/hint/', HintAnswering.as_view(), name='answer hint'),
]

app_name = 'Account'
