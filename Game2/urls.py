from django.urls import path


from .view.submitview import get_problem_from_group, is_problem_gotten_from_group, \
    submit_answer, notification_to_all
from Game2.view.account import NotificationView, TeamView, NextRoomView, PreviousRoomView, StartGameView

urlpatterns = [
    path('get_problem_from_group/<int:gid>/', get_problem_from_group),
    path('is_problem_gotten_from_group/<int:gid>/', is_problem_gotten_from_group),
    path('submit_answer/<int:sid>/<int:pid>/', submit_answer),

    path('notification/', NotificationView.as_view(), name='team notification'),
    path('team/', TeamView.as_view(), name='team info'),
    path('room/next/', NextRoomView.as_view(), name='go to next room'),
    path('room/previous/', PreviousRoomView.as_view(), name='go to prev room'),
    path('room/start/', StartGameView.as_view(), name='go to first room'),

    path('notification_to_all/', notification_to_all),
]
