import strawberry

from djapps.team.models import Tournament
from djapps.team.types.django_types import TournamentType
from djapps.team.types.graphgql_types import  DeleteItemResult


@strawberry.type
class Mutation:
    
        
    @strawberry.mutation
    def create_tournament(
        self,
        name: str,
        description: str
    ) -> TournamentType:
        """
        Create a new tournament.
        """
        tournament = Tournament.objects.create(name=name, description=description)
        return tournament
    
    @strawberry.mutation
    def update_tournament(
        self,
        id: strawberry.ID,
        name: str = None,
        description: str = None
    ) -> TournamentType:
        """
        Update an existing tournament.
        """
        try:
            tournament = Tournament.objects.get(id=id)
            if name is not None:
                tournament.name = name
            if description is not None:
                tournament.description = description
            tournament.save()
            return tournament
        except Tournament.DoesNotExist:
            raise ValueError(f"Tournament with id {id} does not exist.")
        
    @strawberry.mutation
    def delete_tournament(self, id: strawberry.ID) -> DeleteItemResult:
        """
        Delete a tournament by ID.
        """
        try:
            tournament = Tournament.objects.get(id=id)
            tournament.delete()
            return DeleteItemResult(
                success=True, 
                message=f"Tournament with id {id} has been deleted."
            )
        except Tournament.DoesNotExist:
            raise ValueError(f"Tournament with id {id} does not exist.")
        
