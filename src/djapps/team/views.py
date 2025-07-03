from django.shortcuts import render
from .schema import schema
from strawberry.django.views import GraphQLView

# Create your views here.

def home(request):
    template_name = "team/home.html"
    return render(request, template_name)

graphql_view = GraphQLView.as_view(
    schema = schema
)


