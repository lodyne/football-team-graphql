from django.http import HttpResponse
from .schema import schema
from strawberry.django.views import GraphQLView

# Create your views here.

def home(request):
    return HttpResponse("<h1>Welcome to the Team Management GraphQL API</h1>")

graphql_view = GraphQLView.as_view(
    schema = schema
)


