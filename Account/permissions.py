from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions
from rest_framework.permissions import BasePermission
from django.utils.translation import gettext as _
from Game2.models import Team
from Account.models import User
from Game2.utils import get_user_team

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