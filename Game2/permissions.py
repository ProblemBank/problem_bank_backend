from rest_framework import permissions
from .utils import get_user_team
from django.utils.translation import gettext as _
from constants import MAXIMUM_TIME_TO_PLAY
import time


class IsAllowedTOPlay(permissions.BasePermission):
    message = _("زمان مجاز شما برای بازی کردن به پایان رسیده است.")

    def has_permission(self, request, view):
        team = get_user_team(user=request.user)
        if time.time() - team.first_entrance < MAXIMUM_TIME_TO_PLAY:
            return True
        else:
            return False
