import strawberry
from djapps.team.models import PlayerTournament, Player, Tournament
from djapps.team.types.django_types import PlayerTournamentType


@strawberry.type
class Mutation:
    

    @strawberry.mutation
    def create_player_tournament(
        self,
        player_id: strawberry.ID,
        tournament_id: strawberry.ID,
        goals: int = 0,
        assists: int = 0
    ) -> 'PlayerTournamentType':
        """
        Create a new player match record.
        """
        try:
            player = Player.objects.get(id=player_id)
            tournament = Tournament.objects.get(id=tournament_id)
            player_tournament = PlayerTournament.objects.create(
                player=player,
                tornament=tournament,
                goals=goals,
                assists=assists
            )
            return player_tournament
        except (Player.DoesNotExist, Tournament.DoesNotExist) as e:
            raise ValueError(str(e) )