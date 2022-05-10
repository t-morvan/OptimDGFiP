"""
Creation fichier IRIS
"""

import geopandas as gpd
import pandas as pd

from dgfip import paths
from dgfip.structures import add_distances


def get_iris(compute_distance: bool | None = True) -> gpd.GeoDataFrame:

    iris = gpd.read_file(f"../data/{paths.IRIS}")
    rec = pd.read_csv(
        f"../data/{paths.RECENSEMENT}",
        sep=";",
        dtype={"IRIS": str, "COM": str, "LAB_IRIS": str},
    )

    # convert to str before merging
    rec["IRIS"] = rec["IRIS"].str.ljust(9, fillchar="0")

    iris = iris.drop(columns="IRIS")
    iris_enrichi = iris.merge(rec, left_on="CODE_IRIS", right_on="IRIS")

    if compute_distance:
        iris_enrichi = add_distances(iris_enrichi)

    return iris_enrichi
