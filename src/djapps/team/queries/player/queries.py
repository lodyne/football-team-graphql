import strawberry

from djapps.team.models import Player
from djapps.team.services import retrieve_player_with_specific_age
from djapps.team.types.django_types import PlayerType
from strawberry.types import Info


@strawberry.type
class Query:
    
    @strawberry.field
    def player_list(self, info:Info) -> list[PlayerType]:
        """_summary_

        Args:
            info (Info): _description_

        Returns:
            PlayerType: _description_
        """
        
        return Player.objects.all()
    
    @strawberry.field
    def player_by_id(self, info: Info, id: strawberry.ID) -> PlayerType:
        """
        Get a player by ID.
        """
        try:
            player = Player.objects.filter(id=id).first()
            return player
        except PlayerType.DoesNotExist:
            raise ValueError(f"Player with id {id} does not exist.")

    @strawberry.field
    def player_by_squad(self, info: Info, squad_id: strawberry.ID) -> list[PlayerType]:
        """
        Get players by squad ID.
        """
        try:
            players = Player.objects.filter(squad_id=squad_id)
            return players
        except Player.DoesNotExist:
            raise ValueError(f"No players found for squad with id {squad_id}.") 
        
    
        
    @strawberry.field
    def players_by_age(
        self,
        info: Info,
        age : int) -> list[PlayerType]:
        """
        Get players by age.
        """
        
        try:
            players = retrieve_player_with_specific_age(age)
            if not players:
                return []
            if not isinstance(players, list):
                players = [players]
            return players
        except Player.DoesNotExist:
            raise ValueError(f"No players found with age {age}.")
    
    
    