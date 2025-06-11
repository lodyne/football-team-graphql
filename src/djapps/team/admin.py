from django.contrib import admin
from .models import (
    Squad,
    League,
    Tournament,
    Player,
    Coach,
    PlayerMatch,
    Match,
    PlayerTournament,
)

# Register your models here.
admin.site.register(Squad)
admin.site.register(League)
admin.site.register(Tournament)
admin.site.register(Player)
admin.site.register(Coach)
admin.site.register(PlayerMatch)
admin.site.register(Match)
admin.site.register(PlayerTournament)


class SquadAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'size', 'description')
    search_fields = ('name',)
    list_filter = ('size',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('squad_leader')
