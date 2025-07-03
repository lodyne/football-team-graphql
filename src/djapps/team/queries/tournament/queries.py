import strawberry

from djapps.team.models import Tournament
from djapps.team.types.django_types import TournamentType
from strawberry.types import Info

@strawberry.type
class Query:
        
    @strawberry.field
    def tournament_list(self, info: Info) -> list[TournamentType]:
        """
        Get all tournaments.
        """
        tournament = Tournament.objects.all() 
        return tournament  
    
    @strawberry.field
    def tournament_by_id(self, info: Info, id: strawberry.ID) -> TournamentType:
        """
        Get a tournament by ID.
        """
        try:
            tournament = Tournament.objects.get(id=id)
            return tournament
        except Tournament.DoesNotExist:
            raise ValueError(f"Tournament with id {id} does not exist.")
        