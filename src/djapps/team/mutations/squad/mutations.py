
import strawberry

from djapps.team.models import League, Squad, Venue
from djapps.team.services import create_squad_service
from djapps.team.types.django_types import SquadType



@strawberry.type
class Mutation:
    
    @strawberry.mutation
    def create_squad(
        self, 
        name: str,
        size: int, 
        league_id: strawberry.ID,
        description: str = "", 
        venue_id: strawberry.ID = None
    ) -> SquadType:
        """
        Create a new squad.
        """
        try:
            # Only check existence, don't pass model instances to the service
            if venue_id is not None:
                if not Venue.objects.filter(id=venue_id).exists():
                    raise ValueError(f"Venue with id {venue_id} does not exist.")
            if not League.objects.filter(id=league_id).exists():
                raise ValueError(f"League with id {league_id} does not exist.")

            squad = create_squad_service(
                name, 
                size, 
                int(league_id), 
                description, 
                int(venue_id) if venue_id is not None else None
            )
        except Exception as e:
            raise ValueError(f"An error occurred while creating the squad: {str(e)}")

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
    

    