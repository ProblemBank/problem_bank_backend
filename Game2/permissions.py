from rest_framework import permissions
import time
from Game2.models import GameInfo
from .utils import get_user_team


class IsAllowedTOPlay(permissions.BasePermission):
    message = "زمان مجاز شما برای بازی کردن به پایان رسیده است."

    def has_permission(self, request, view):
        self.message = 'زمان مجاز شما برای بازی به پایان رسیده است.'
        team = get_user_team(user=request.user)
        if time.time() - team.first_entrance < GameInfo.objects.get(id=1).max_time_to_play:
            return True
        else:
            return False


class IsAllowedToOpenBox(permissions.BasePermission):
    message = 'طبق قوانین بازی نمی‌توانید این جعبه را باز کنید.'

    def has_permission(self, request, view):
        user = request.user
        team = get_user_team(user)
        current_room = team.current_room
        if current_room.name == GameInfo.objects.get(id=1).last_room_name:
            return True
        else:
            return False
