from django.urls import path


from .view.submitview import get_problem_from_group, is_problem_gotten_from_group, \
    submit_answer, notification_to_all, judge_view
from Game2.view.account import NotificationView, TeamView, RoomView, BoxView

from Game2.view.account import NotificationView, TeamView, RoomView
from Game2.view.carrousel_view import turnning_carrousel

urlpatterns = [
    path('get_problem_from_group/<int:gid>/', get_problem_from_group),
    path('is_problem_gotten_from_group/<int:gid>/', is_problem_gotten_from_group),
    path('submit_answer/<int:sid>/<int:pid>/', submit_answer),
    path('judge/<int:sid>/<int:mark>/', judge_view),

    path('notification/', NotificationView.as_view(), name='team notification'),
    path('team/', TeamView.as_view(), name='team info'),
    path('room/<str:r_name>/', RoomView.as_view(), name='go to next room'),
    path('box/<int:bid>/', BoxView.as_view(), name='open box'),

    path('notification_to_all/', notification_to_all),
    path('turnning_carrousel/', turnning_carrousel),
]
