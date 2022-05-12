"""
Distance aux centres DGFIP
"""

import geopandas as gpd
import pandas as pd

from dgfip.read import get_iris, get_dep


def mean_distances(
    categories: list[str] | None = None, save: bool = False
) -> gpd.GeoDataFrame:
    """
    Calcul de la distance moyenne des IRIS d'un département aux services DGFIP les plus proches
    Pondération par la population
    """
    if categories is None:
        categories = ["P17_POP", "P17_POP80P"]

    iris = get_iris()
    dep = get_dep(crs="2154")

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

    # rajout des infos spatiales
    base = dep.merge(agg, left_on="code", right_on="DEP")

    if save:
        base.to_file("../data/departement_distances.geojson", driver="GeoJSON")

    return base
