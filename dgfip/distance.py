"""
Distance aux centres DGFIP
"""

from typing import List, Optional

import geopandas as gpd
import pandas as pd

from dgfip.read import get_iris, add_distances


def mean_distances(
    categories: Optional[List[str]] = None,
    public: str | None = None,
    filename: str | None = None,
) -> gpd.GeoDataFrame:
    """
    Calcul de la distance moyenne des IRIS d'un département aux services DGFIP les plus proches
    Pondération par la population
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
        agg.to_csv(f"../data/{filename}")

    return agg
