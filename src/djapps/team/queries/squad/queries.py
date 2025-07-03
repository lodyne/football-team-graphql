import strawberry


from strawberry.types import Info

from djapps.team.models import Squad
from djapps.team.types.django_types import SquadType

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
        
    