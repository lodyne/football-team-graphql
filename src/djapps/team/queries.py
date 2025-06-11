import strawberry

from djapps.team.exceptions import ErrorByIdResponse, ErrorException
from djapps.team.services import retrieve_player_with_specific_age
from .models import (
    Coach, 
    League, 
    Player, 
    Squad, 
    Tournament,
    Venue,
    Match
)
from strawberry.types import Info
from .types.django_types import CoachType, LeagueType, MatchType, PlayerType, SquadType, TournamentType, VenueType

@strawberry.type
class Query:
    @strawberry.field
    def squad_list(self, info: Info) -> list[SquadType]:
        """
        Get all squad.
        """
        return Squad.objects.all()
    
    @strawberry.field
    def squad_by_id(self,info:Info, id: strawberry.ID) -> SquadType:
        """
        Get a squad by ID.
        """
        try:
            squad = Squad.objects.get(id=id)
            return squad
        except Squad.DoesNotExist:
            raise ValueError(f"Squad with id {id} does not exist.")
        
    @strawberry.field
    def league_list(self, info:Info) -> list[LeagueType]:
        """
        Get all leagues.
        """
        return League.objects.all()
    
    @strawberry.field
    def league_by_id(self,info : Info, id : strawberry.ID) -> LeagueType:
        try:
            league= League.objects.filter(id=id).first()
            return league
        except League.DoesNotExist:
            raise ValueError(f"League with id:{id} does not exist")
        
    @strawberry.field
    def coach_list(self, info:Info, order: str = None) -> list[CoachType]:
        """
        Get all coaches.
    
        """
        queryset = Coach.objects.all()
        
        if order in ["id","-id"]:  
            queryset = queryset.order_by(order)     
        return queryset
            
    @strawberry.field
    def coach_by_id(self, info: Info, id: strawberry.ID) -> CoachType:
        """
        Get a coach by ID.
        """
        try:
            coach = Coach.objects.get(id=id)
            return coach
        except Coach.DoesNotExist:
            raise ValueError(f"Coach with id {id} does not exist.")
    
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
        
    @strawberry.field
    def venue_list(self, info: Info) -> list['VenueType']:
        """
        Get all venues.
        """
        return Venue.objects.all()

    @strawberry.field   
    def order_venue(self, info: Info, order_by: str = "id") -> list['VenueType']:
        """
        Get all venues.
        """
        return Venue.objects.all() .order_by(order_by)
    
    @strawberry.field
    def venue_by_id(self, info: Info, id: strawberry.ID) -> 'VenueType':
        """
        Get a venue by ID.
        """
        try:
            venue = Venue.objects.get(id=id)
            return venue
        except Venue.DoesNotExist:
            raise ValueError(f"Venue with id {id} does not exist.")  

    @strawberry.field
    def venue_by_squad(
        self, 
        info: Info,
        squad_name : str = None,
        squad_id : strawberry.ID = None) -> VenueType:
        """
        Get a venue by squad ID.
        
        """
        if not squad_name and not squad_id:
            raise ValueError("Either squad_name or squad_id must be provided.")
        try:
            if squad_name:
                squad = Squad.objects.get(name=squad_name)
            else:
                squad = Squad.objects.get(id=squad_id)
            venue = squad.home_venue
            if not venue:
                raise ValueError("No home venue set for this squad")
            return venue
        except Venue.DoesNotExist:
            return ErrorByIdResponse(
                ok=False,
                error=ErrorException(
                    message=f"Venue with squad name {squad_name} or id {squad_id} does not exist.",
                    code="NOT_FOUND"
                )
            )
            # raise ValueError("No venue found for  this squad")
        
    @strawberry.field
    def venue_by_squad_name(
        self, 
        info: Info, 
        squad_name: str,
        ) -> VenueType:
        """
        Get a venue by squad name.
        """
        try:
            squad = Squad.objects.get(name=squad_name)
            venue = squad.home_venue
            if not venue:
                raise ValueError(f"No home venue set for squad with name {squad_name}.")
            return venue
        except Squad.DoesNotExist:
            raise ValueError(f"Squad with name {squad_name} does not exist.")
        
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
    
    @strawberry.field
    def match_list(self, info: Info) -> list['MatchType']:
        """
        Get all matches.
        """
        return Match.objects.all()
    
    @strawberry.field
    def match_by_id(self, info: Info, id: strawberry.ID) -> list['MatchType']:
        """
        Get all matches.
        """
        try:
            match = Match.objects.filter(id=id).first() 
            return match
        except Match.DoesNotExist:
            raise ValueError(f"Match with id {id} does not exist.")
        