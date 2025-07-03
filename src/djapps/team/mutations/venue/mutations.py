import strawberry

from djapps.team.exceptions import ErrorByIdResponse, ErrorException
from djapps.team.models import Venue
from djapps.team.types.django_types import VenueType
from djapps.team.types.graphgql_types import DeleteItemResult


@strawberry.type
class Mutation:
    
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
