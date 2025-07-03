import strawberry


from strawberry.types import Info

from djapps.team.models import PlayerTournament
from djapps.team.types.django_types import PlayerTournamentType


@strawberry.type
class Query:

    @strawberry.field
    def player_tournament_list(
        self, 
        info: Info)  -> list['PlayerTournamentType'] :
        """
        Get all tournaments for a player.
        """
        try:
            player_tournaments = PlayerTournament.objects.all()
            return player_tournaments
        except PlayerTournament.DoesNotExist:
            raise ValueError("No tournaments found for player does not exist.")