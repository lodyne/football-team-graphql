import strawberry

from djapps.team.models import Player, Squad
from djapps.team.types.django_types import PlayerType
from djapps.team.types.graphgql_types import DeleteItemResult



@strawberry.type
class Mutation:
    
    
    @strawberry.mutation
    def create_player(
        self,
        name: str,
        squad_id: strawberry.ID,
        position: str,
        age: int,
        nationality: str
    ) -> PlayerType:
        
        """
        Create a new player for a squad.
        """
        try:
            squad = Squad.objects.get(id=squad_id)
        except Squad.DoesNotExist:
            raise ValueError(f"Squad with id {squad_id} does not exist.")
        
        player = Player.objects.create(
            name=name,
            squad=squad,
            position=position,
            age=age,
            nationality=nationality)
        return player
    
    @strawberry.mutation
    def update_player(
        self,
        id: strawberry.ID,
        name: str = None,
        squad_id: strawberry.ID = None,
        position: str = None,
        age: int = None,
        nationality: str = None
    ) -> PlayerType:
        """
        Update an existing player.
        
        """
        try:
            # player = Player.objects.get(id=id)
            player = Player.objects.filter(id=id).first()
            print(f"Updating player: {player} with ID: {id}")
            if name is not None:
                player.name = name
            if squad_id is not None:
                try:
                    squad = Squad.objects.get(id=squad_id)
                    player.squad = squad
                except Squad.DoesNotExist:
                    raise ValueError(f"Squad with id {squad_id} does not exist.")
            if position is not None:
                player.position = position
            if age is not None:
                player.age = age
            if nationality is not None:
                player.nationality = nationality
            player.save()
        except Player.DoesNotExist:
            raise ValueError(f"Player with id {id} does not exist.")
        return player
    
    @strawberry.mutation
    def delete_player(self, id: strawberry.ID) -> DeleteItemResult:
        """
        Delete a player by ID.
        """
        try:
            player = Player.objects.get(id=id)
            player.delete()
            return DeleteItemResult(
                success=True, 
                message=f"Player with id {id} has been deleted."
            )
        except Player.DoesNotExist:
            raise ValueError(f"Player with id {id} does not exist.")
        
