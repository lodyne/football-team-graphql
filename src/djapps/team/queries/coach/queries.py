import strawberry


from strawberry.types import Info

from djapps.team.models import Coach
from djapps.team.types.django_types import CoachType

@strawberry.type
class Query:
    
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
    
    