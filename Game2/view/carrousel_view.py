from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from Game2.utils import get_user_team
import random
from constants import CARROUSEL_REWARD_RATIO_FOR_WIN, CARROUSEL_REWARD_RATIO_FOR_LOSE
from rest_framework import status
from Game2.permissions import IsAllowedTOPlay
from Game2.models import GameInfo

@permission_classes([IsAllowedTOPlay])
def turnning_carrousel(user):
    team = get_user_team(user)
    if team.carrousel_turn > 0:
        if random.random() > 0.5:
            team.coin = team.coin * GameInfo.carrousel_win_ratio_reward
            message = "تبریک سکه‌های شما یک و نیم برابر شد"
        else:
            team.coin = team.coin * GameInfo.carrousel_lose_ratio_reward
            message = "متاسفانه سمه‌های شما نصف شد"

        team.carrousel_turn = team.carrousel_turn - 1
        team.save(update_fields=["coin", "carrousel_turn"])
    else:
        message = "تعداد دفعات مجاز چرخاندن به پایان رسیده است."
    return Response({'message': message}, status=status.HTTP_200_OK)

