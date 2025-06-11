from datetime import datetime
import strawberry

from djapps.team.exceptions import ErrorByIdResponse, ErrorException
from djapps.team.services import create_squad_service
from djapps.team.types.graphgql_types import DeleteItemResult
from .models import (
    League, 
    Player,
    Squad, 
    Coach, 
    Tournament, 
    Venue,
    Match
)
    
from .types.django_types import(
    CoachType,
    LeagueType,
    MatchType, 
    PlayerType,
    SquadType, 
    TournamentType, 
    VenueType
) 

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_squad(
        self, 
        name: str,
        size: int, 
        league_id: strawberry.ID,
        description: str = "", 
        ) -> SquadType:
        """
        Create a new squad.
        
        """
        squad = create_squad_service(name, size, league_id, description)
    
        return squad
    
    @strawberry.mutation
    def update_squad(
        self,
        id: strawberry.ID,
        name: str = None,
        size: int = None,
        league_id: strawberry.ID = None,
        description: str = None,
        home_venue_id: strawberry.ID = None
    ) -> SquadType:
        """
        Update an existing squad.
        
        """
        try:
            squad = Squad.objects.get(id=id)
            if name is not None:
                squad.name = name
            if size is not None:
                squad.size = size
            if league_id is not None:
                try:
                    league = League.objects.get(id=league_id)
                    squad.league = league
                except League.DoesNotExist:
                    raise ValueError(f"League with id {league_id} does not exist.")
            if description is not None:
                squad.description = description
            if home_venue_id is not None:
                try:
                    home_venue = Venue.objects.get(id=home_venue_id)
                    squad.home_venue = home_venue
                except Venue.DoesNotExist:
                    raise ValueError(f"Venue with id {home_venue_id} does not exist.")
            squad.save()
            return squad
        except Squad.DoesNotExist:
            raise ValueError(f"Squad with id {id} does not exist.")
    

    @strawberry.mutation
    def create_league(self, name: str, country: str, description: str) -> LeagueType:
        """
        Create a new league.
        """
        league = League.objects.create(name=name,country=country, description=description)
        return league
    

    @strawberry.mutation
    def delete_league(self, id: strawberry.ID) -> DeleteItemResult:
        """
        Delete a league by ID.
        """
        try:
            league = League.objects.get(id=id)
            league.delete()
            message = f"League with id {id} has been deleted."
            return DeleteItemResult(success=True, message=message)
        except League.DoesNotExist:
            raise ValueError(f"League with id {id} does not exist.")
        
    @strawberry.mutation
    def create_coach(
        self,
        name: str,
        squad_id: strawberry.ID
    ) -> CoachType:
        """
        Create a new coach for a squad.
        """
        try:
            squad = Squad.objects.get(id=squad_id)
        except Squad.DoesNotExist:
            raise ValueError(f"Squad with id {squad_id} does not exist.")
        coach = Coach.objects.create(name=name, squad=squad)
        return coach
    
    @strawberry.mutation
    def update_coach(
        self,
        id: strawberry.ID,
        name: str = None,
        squad_id: strawberry.ID = None
    ) -> CoachType:
        """
        Update an existing coach.
        """
        try:
            coach = Coach.objects.get(id=id)
            if name is not None:
                coach.name = name
            if squad_id is not None:
                try:
                    squad = Squad.objects.get(id=squad_id)
                    coach.squad = squad
                except Squad.DoesNotExist:
                    raise ValueError(f"Squad with id {squad_id} does not exist.")
            coach.save()
            return coach
        except Coach.DoesNotExist:
            raise ValueError(f"Coach with id {id} does not exist.")
        
        
    @strawberry.mutation
    def delete_coach(self, id: strawberry.ID) -> bool:
        """
        Delete a coach by ID.
        """
        try:
            coach = Coach.objects.get(id=id)
            coach.delete()
            return True
        except Coach.DoesNotExist:
            raise ValueError(f"Coach with id {id} does not exist.")
    
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
        
        
    @strawberry.mutation
    def create_venue(
        self,
        name : str,
        location:str,
        capacity : int
    ) -> VenueType:
        """
        Create a new venue.
        """
        venue = Venue.objects.create(name=name, location=location, capacity=capacity)
        return venue
    
    @strawberry.mutation
    def update_venue(
        self,
        id: strawberry.ID,
        name: str = None,
        location: str = None,
        capacity: int = None
    ) -> VenueType:
        """
        Update an existing venue.
        """
        try:
            venue = Venue.objects.get(id=id)
            if name is not None:
                venue.name = name
            if location is not None:
                venue.location = location
            if capacity is not None:
                venue.capacity = capacity
            venue.save()
            return venue
        except Venue.DoesNotExist:
            return ErrorByIdResponse(
                ok=False,
                errors=ErrorException(
                    message=f"Venue with id {id} does not exist.",
                    code="VENUE_NOT_FOUND"
                )
            )    
            
    @strawberry.mutation
    def delete_venue(self, id: strawberry.ID) -> DeleteItemResult:
        """
        Delete a venue by ID.
        """
        try:
            venue = Venue.objects.get(id=id)
            venue.delete()
            return DeleteItemResult(
                success=True, 
                message=f"Venue with id: {id} has been deleted."
            )
        except Venue.DoesNotExist:
            return ErrorByIdResponse(
                ok=False,
                error=ErrorException(
                    message=f"Venue with id {id} does not exist.",
                    code="VENUE_NOT_FOUND"
                )
            )
    
    @strawberry.mutation
    def create_match(
        self,
        home_team_id: strawberry.ID,
        away_team_id: strawberry.ID,
        date: str,  # Pass date as a datetime object
        venue_id: strawberry.ID,
        score_home: int = 0,
        score_away: int = 0
    ) -> 'MatchType':
        """
        Create a new match.
        """
        try:
            home_team = Squad.objects.get(id=home_team_id)
            away_team = Squad.objects.get(id=away_team_id)
            venue = Venue.objects.get(id=venue_id)
            date_obj = datetime.fromisoformat(date)
            match = Match.objects.create(
                home_team=home_team,
                away_team=away_team,
                date=date_obj,
                venue=venue,
                score_home=score_home,
                score_away=score_away
            )
            return match
        except (Squad.DoesNotExist, Venue.DoesNotExist) as e:
            raise ValueError(str(e))
        
    @strawberry.mutation
    def update_match(
        self,
        id: strawberry.ID,
        home_team_id: strawberry.ID = None,
        away_team_id: strawberry.ID = None,
        date: str = None,  # Pass date as a datetime object
        venue_id: strawberry.ID = None,
        score_home: int = None,
        score_away: int = None
    ) -> MatchType:
        """
        Update an existing match.
        """
        try:
            match = Match.objects.get(id=id)
            if home_team_id is not None:
                match.home_team = Squad.objects.get(id=home_team_id)
            if away_team_id is not None:
                match.away_team = Squad.objects.get(id=away_team_id)
            if date is not None:
                match.date = datetime.fromisoformat(date)
            if venue_id is not None:
                match.venue = Venue.objects.get(id=venue_id)
            if score_home is not None:
                match.score_home = score_home
            if score_away is not None:
                match.score_away = score_away
            match.save()
            return match
        except Match.DoesNotExist:
            raise ValueError(f"Match with id {id} does not exist.")
        
    @strawberry.mutation
    def delete_match(self, id: strawberry.ID) -> DeleteItemResult:
        """
        Delete a match by ID.
        """
        try:
            match = Match.objects.get(id=id)
            match.delete()
            return DeleteItemResult(
                success=True, 
                message=f"Match with id {id} has been deleted."
            )
        except Match.DoesNotExist:
            raise ValueError(f"Match with id {id} does not exist.")
