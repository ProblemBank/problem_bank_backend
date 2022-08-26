from rest_framework import permissions
from .utils import get_user_team
from django.utils.translation import gettext as _

import time
MAXIMUM_TIME_TO_PLAY = 4 * 60 * 60


class IsAllowedTOPlay(permissions.BasePermission):
    message = _("زمان مجاز شما برای بازی کردن به پایان رسیده است.")

    def has_permission(self, request):
        team = get_user_team(user=request.user)
        if time.time() - team.first_entrance > MAXIMUM_TIME_TO_PLAY:
            return True
        else:
            return False
