"""
Ischrone computations
"""
from typing import Tuple

import geopandas as gpd
import routingpy
from shapely.geometry import Polygon


def get_isochrone(
    client: routingpy.routers.Valhalla, location: Tuple[float, float], duration: int
) -> gpd.GeoDataFrame:

    iso = client.isochrones(locations=location, profile="auto", intervals=duration)
    iso_df = gpd.GeoDataFrame(
        {"id": [x for x in range(len(iso))]},
        geometry=[Polygon(X.geometry) for X in reversed(iso)],
        crs="EPSG:4326",
    )
    return iso_df
