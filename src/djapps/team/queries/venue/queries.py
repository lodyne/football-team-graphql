import strawberry

from strawberry.types import Info

from djapps.team.exceptions import ErrorByIdResponse, ErrorException
from djapps.team.models import Squad, Venue
from djapps.team.types.django_types import VenueType


@strawberry.type
class Query:
        
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
        
    