from django.contrib import admin

# Register your models here.


from .models import Room, Box, Team, TeamBox, GameInfo, Answer, Carrousel, Notification


admin.site.register(TeamBox)
admin.site.register(GameInfo)
admin.site.register(Room)
admin.site.register(Box)
admin.site.register(Team)
admin.site.register(Answer)
admin.site.register(Carrousel)
admin.site.register(Notification)
