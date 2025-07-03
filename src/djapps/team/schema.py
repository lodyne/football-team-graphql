import strawberry

from djapps.team.queries import Query


from djapps.team.mutations import Mutation


schema = strawberry.Schema(query=Query,mutation=Mutation)