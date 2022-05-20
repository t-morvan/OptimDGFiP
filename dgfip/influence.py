import geopandas as gpd
import numpy as np
from libpysal.cg.voronoi import voronoi_frames
from shapely.geometry import box

from dgfip import paths
from dgfip.read import get_iris, get_structures


def tessalate(
    sources: gpd.GeoDataFrame, background: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    """
    Crée une tessalation en cellule de Voronoi

    Args:
        sources: points sources pour construire le diagramme de Voronoi
        background: limites du diagramme

    Returns:
        cellules du diagramme
    """
    x = np.array(sources.to_crs(crs="2154").geometry.x)
    y = np.array(sources.to_crs(crs="2154").geometry.y)
    points = np.stack((x, y), axis=-1)

    points_u = np.unique(points, axis=0)
    zones, _ = voronoi_frames(points_u, clip=box(*background.total_bounds))

    zones = zones.set_crs("2154").clip(background)

    return zones


def create_influence(
    service: str = "Centre de Finances publiques", save: bool = False
) -> gpd.GeoDataFrame:
    """
    Creation des zones d'influence des services DGFIP

    Args:
        service: sélection du type de service
        save: si vrai, sauvegarde le fichier au format geojson

    returns:
        base des zones d'influences enrichies des informations démographiques
    """
    # creation des zones
    structures = get_structures(crs="2154")
    centres = structures[structures["TYPE DE SERVICE"] == service]
    dep = gpd.read_file(f"../data/{paths.DEP}", crs="4326")
    dep = dep.to_crs("2154")
    zones = tessalate(centres, dep)

    # ajout des informations IRIS
    zones["id"] = zones.index
    iris = get_iris()
    inter = zones.sjoin(iris)
    agg = inter.groupby("id").sum()
    sources = gpd.GeoDataFrame(agg, geometry=zones.geometry)
    sources["area"] = zones.area / 10**6
    sources = sources.to_crs("4326")

    if save:
        name = f"data/influence_{service.replace(' ','')}.geojson"
        sources.to_file(name, driver="GeoJSON")

    return sources
