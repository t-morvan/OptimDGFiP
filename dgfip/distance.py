"""
Distance aux centres DGFIP
"""

from typing import List, Optional

import geopandas as gpd
import pandas as pd

from dgfip.read import get_iris, get_structures


def add_distances(
    sources: gpd.GeoDataFrame, inside: None | bool = True, public: str | None = None
) -> gpd.GeoDataFrame:
    """
    Calcule la distance (km) à la structure DGFIP la plus proche,
    pour chaque source et type de service.
    Rajoute les colonnes correspondantes.

    Args:
        sources: geodataframe des sources
        inside: si vrai, rajoute pour chaque source si elle contient une structure DGFIP

    Returns:
        le geodataframe enrichi des distances
    """

    # conversion en Lambert 93 pour le calcul des distances
    if sources.crs.to_epsg() != "2154":
        sources = sources.to_crs("2154")

    structures = get_structures(crs="2154")
    # selection du public si précisé
    if public is not None:
        if public not in {"particuliers", "professionnels"}:
            raise ValueError(
                "Public prend les valeurs 'particuliers' ou 'professionnels' "
            )
        structures = structures[structures["public"].str.contains(public, na=False)]

    # par type de service
    for name, service in structures.groupby("TYPE DE SERVICE"):
        sources[f"distance {name}"] = (
            service.sindex.nearest(
                sources.geometry, return_distance=True, return_all=False
            )[1]
            / 1000
        )
        if inside:
            sources[f"intersect {name}"] = sources[f"distance {name}"].eq(0)

    # service autre que buralistes
    nonburalistes = structures[structures["TYPE DE SERVICE"] != "Buralistes"]
    sources["distance non Buralistes"] = (
        nonburalistes.sindex.nearest(
            sources.geometry, return_distance=True, return_all=False
        )[1]
        / 1000
    )
    if inside:
        sources["intersect non Buralistes"] = sources["distance non Buralistes"].eq(0)

    return sources


def mean_distances(
    categories: Optional[List[str]] = None,
    public: str | None = None,
    filename: str | None = None,
) -> gpd.GeoDataFrame:
    """
    Calcul de la distance moyenne des IRIS
    d'un département aux services DGFiP les plus proches
    Pondération par la catégorie de population

    Args:
        categories: catégories de population à prendre en compte
        public: "professionnels" ou "particuliers", filtre les structures DGFiP proposant un service à ce public
        filename: nom sous lequel la base sera sauvegardée

    Returns:
        Base des distances moyennes par département et catégorie.

    Example :
    >>> mean_distance(["P17_POP", "P17_POP80P"], 'particuliers', 'distances_pop_particuliers.csv')

    """
    if categories is None:
        categories = ["P17_POP", "P17_POP80P"]

    iris = get_iris()
    iris = add_distances(iris, public=public)

    # melt à améliorer
    long_iris = pd.melt(
        iris,
        value_vars=[col for col in iris.columns if col.startswith("distance")],
        id_vars=["CODE_IRIS"] + categories,
        var_name="service",
        value_name="distance",
    )
    long_iris["service"] = long_iris["service"].str.replace("distance ", "")

    long_iris = pd.melt(
        long_iris,
        id_vars=["CODE_IRIS", "service", "distance"],
        value_name="pop",
        var_name="pop_cat",
    )

    # agregation
    long_iris["prod"] = long_iris["pop"] * long_iris["distance"]
    long_iris["DEP"] = long_iris["CODE_IRIS"].str.slice(0, 2)

    agg = long_iris.groupby(["DEP", "service", "pop_cat"]).sum().reset_index()
    agg["distance_avg"] = agg["prod"] / agg["pop"]
    agg = agg[["DEP", "distance_avg", "service", "pop_cat"]]

    if filename is not None:
        agg.to_csv(f"data/{filename}")

    return agg
