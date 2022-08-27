from django.contrib import admin

# Register your models here.


from .models import Room, Box, Team, TeamBox, GameInfo, Carrousel, Notification, TeamBox, TeamRoom


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'coin', 'first_entrance']


admin.site.register(TeamBox)
admin.site.register(GameInfo)
admin.site.register(Room)
admin.site.register(Box)
admin.site.register(Carrousel)
admin.site.register(Notification)
admin.site.register(TeamRoom)
