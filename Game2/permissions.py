from rest_framework import permissions
from django.utils.translation import gettext as _
import time
from Game2.models import GameInfo
from .utils import get_user_team


class IsAllowedTOPlay(permissions.BasePermission):
    message = _("زمان مجاز شما برای بازی کردن به پایان رسیده است.")

    def has_permission(self, request, view):
        team = get_user_team(user=request.user)
        if time.time() - team.first_entrance < GameInfo.objects.get(id=1).max_time_to_play:
            return True
        else:
            return False


class IsAllowedToOpenBox(permissions.BasePermission):
    message = _('طبق قوانین بازی نمی‌توانید این جعبه را باز کنید.')

    def has_permission(self, request, view):
        user = request.user
        team = get_user_team(user)
        current_room = team.current_room
        if current_room.name == GameInfo.objects.get(id=1).last_room_name:
            return True
        else:
            return False
