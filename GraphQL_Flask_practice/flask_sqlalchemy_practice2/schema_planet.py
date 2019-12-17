from graphene_sqlalchemy import SQLAlchemyObjectType
from database.model_planet import ModelPlanet
import graphene


# Create a generic class to mutualize description of planet attributes for both queries and mutations
class PlanetAttribute:
    name = graphene.String(description="Name of the planet.")
    rotation_period = graphene.String(description="Rotation period of the planet.")
    orbital_period = graphene.String(description="Orbital period of the planet.")
    diameter = graphene.String(description="Diameter of the planet.")
    climate = graphene.String(description="Climate period of the planet.")
    gravity = graphene.String(description="Gravity of the planet.")
    terrain = graphene.String(description="Terrain of the planet.")
    surface_water = graphene.String(description="Surface water of the planet.")
    population = graphene.String(description="Population of the planet.")
    url = graphene.String(description="URL of the planet in the Star Wars API.")


class Planet(SQLAlchemyObjectType, PlanetAttribute):
    """Planet node."""

    class Meta:
        model = ModelPlanet
        interfaces = (graphene.relay.Node,)
