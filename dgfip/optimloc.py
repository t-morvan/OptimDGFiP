"""
Re-localisation des structures DGFIP pour minimiser les distances
"""

from typing import List, Set

import geopandas as gpd
import numpy as np
import pandas as pd
from joblib import cpu_count
from numpy import typing as npt
from sklearn.cluster import MiniBatchKMeans

from dgfip.read import get_iris, get_structures


def optimize(points: npt.NDArray, nsources: int, weight: npt.NDArray) -> npt.NDArray:
    """
    Perform Mini batch kmeans

    Args:
        points: coordinates array
        nsources: number of sources to place
        weight: sample weight array

    Returns:
        position coordinates
    """

    kmeans = MiniBatchKMeans(
        n_clusters=nsources,
        batch_size=256 * cpu_count(),
        n_init=10,
        max_no_improvement=10,
    )

    kmeans.fit(points, weight)

    return kmeans.cluster_centers_


def preprocess(service: str, categories: List[str], deps):
    """
    Preprocess data in order to perform kmeans

    Args:
        service: type de service
        categories: categories de population
        deps: departements à traiter

    Returns:
        nombre de sources à placer, coordonnées des centroides des IRIS, populations des IRIS
    """

    # nombre de structures avec des adresses distinctes
    # dans la region s'adressant aux particuliers
    structures = get_structures(crs="2154")
    structures_selec = structures[
        (structures["TYPE DE SERVICE"] == service)
        & structures["public"].str.contains("particuliers")
        & structures["DEPARTEMENT"].isin(deps)
    ]
    nsources = structures_selec["ADRESSE"].nunique()

    iris = get_iris()
    iris_region = iris[iris["INSEE_COM"].str.slice(0, 2).isin(deps)]
    centroids_iris = iris_region.centroid

    points = np.array([centroids_iris.x, centroids_iris.y]).T
    weights = np.array([iris_region[categorie].values for categorie in categories])

    return nsources, points, weights, structures_selec


def relocate(
    service: str = "Centre de Finances publiques",
    save: bool = False,
    categories: List[str] | None = None,
    deps: Set[str] | None = None,
):

    # par chauvinisme
    if deps is None:
        deps = {"22", "29", "35", "56"}

    if categories is None:
        categories = ["P17_POP", "P17_POP80P", "C17_POP15P_CS7"]

    nsources, points, weights, structures = preprocess(service, categories, deps)

    geo_list = []
    for weight, categorie in zip(weights, categories):
        centers = optimize(points, nsources, weight)
        geo = gpd.points_from_xy(*centers.T)
        serie = pd.Series([categorie] * len(geo), name="categorie")
        geo_df = gpd.GeoDataFrame(serie, geometry=geo, crs="2154")
        geo_list.append(geo_df)

    structures["categorie"] = "initial"
    geo_list.append(structures[["categorie", "geometry"]])
    loc = gpd.GeoDataFrame(pd.concat(geo_list, ignore_index=True), crs="2154")
    loc = loc.to_crs("4326")

    if save:
        loc.to_file("../data/reloc.geojson", driver="GeoJSON")

    return loc
