import pytest
from django.urls import reverse
from django.test import Client
from djapps.team.models import Squad, League, Player


@pytest.mark.django_db
def test_homepage_loads():
    client = Client()
    response = client.get(
        reverse("home")
    )  # Make sure 'home' is the correct name for your home view
    assert response.status_code == 200
    assert b"Team Management GraphQL API" in response.content


@pytest.mark.django_db
def test_create_league():
    league = League.objects.create(
        name="Premier League", country="England", description="Top English league"
    )
    assert League.objects.count() == 1
    assert league.name == "Premier League"


@pytest.mark.django_db
def test_create_squad():
    league = League.objects.create(
        name="Serie A", country="Italy", description="Italian league"
    )
    squad = Squad.objects.create(
        name="Juventus", size=25, description="Top Italian club", league=league
    )
    assert Squad.objects.count() == 1
    assert squad.league.name == "Serie A"


@pytest.mark.django_db
def test_create_player():
    league = League.objects.create(
        name="La Liga", country="Spain", description="Spanish league"
    )
    squad = Squad.objects.create(
        name="Barcelona", size=23, description="Spanish club", league=league
    )
    player = Player.objects.create(
        name="Messi", squad=squad, position="Forward", age=34, nationality="Argentina"
    )
    assert Player.objects.count() == 1
    assert player.squad.name == "Barcelona"
    assert player.position == "Forward"
