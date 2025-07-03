from datetime import datetime
import strawberry

from djapps.team.models import Match, Squad, Venue
from djapps.team.types.django_types import MatchType
from djapps.team.types.graphgql_types import DeleteItemResult



@strawberry.type
class Mutation:
    
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

    