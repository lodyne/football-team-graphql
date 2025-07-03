import strawberry

from djapps.team.constants import COACH_CREATED_SUCCESS
from djapps.team.types.graphgql_types import CoachResponse
from djapps.team.types.django_types import CoachType
from djapps.team.models import Coach, Squad
    


@strawberry.type
class Mutation:
    

    @strawberry.mutation
    def create_coach(
        name: str,
        squad_id: strawberry.ID
    ) -> CoachResponse:
        """
        Create a new coach for a squad.
        """
        try:
            squad = Squad.objects.get(id=squad_id)
            coach = Coach.objects.create(name=name, squad=squad)
            return CoachResponse(
                ok = True,
                message = COACH_CREATED_SUCCESS,
                coach = coach
            )
        except Squad.DoesNotExist:
            return CoachResponse(
                ok=False,
                message=f"Squad with id {squad_id} does not exist.",
                coach=None
            )
    
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
    

    

        
        
