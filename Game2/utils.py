from Game2.models import Team
from Game2.models import Room
from Game2.models import TeamRoom
from Account.models import User


def create_team_room(team: Team):
    rooms = Room.objects.all()
    first_room = rooms.first()
    for room in rooms:
        if not TeamRoom.objects.filter(team=team, room=room).exists():
            TeamRoom.objects.create(room=room, team=team)
            team.current_room = first_room
            team.save()


def get_user_team(user: User) -> Team:
    team = Team.objects.filter(users__in=[user]).first()
    return team
