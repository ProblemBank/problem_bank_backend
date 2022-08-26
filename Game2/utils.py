from Game2.models import Team
from Account.models import User

def get_user_team(user:User) -> Team:
    team = Team.objects.filter(users__in=[user]).first()
    return team