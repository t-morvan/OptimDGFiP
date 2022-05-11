"""
Construction de la base communale
"""

import pandas as pd
import geopandas as gpd

from dgfip import paths
from dgfip.structures import add_distances


def get_com() -> gpd.GeoDataFrame:

    com = gpd.read_file(f"../data/{paths.COM}")
    rec = pd.read_csv(
        f"../data/{paths.RECENSEMENT_COM}", sep=";", dtype={"CODGEO": str}
    )
    rev = pd.read_csv(
        f"../data/{paths.REVENUS_COM}",
        sep=";",
        dtype={"CODGEO": str},
        usecols=["CODGEO", "MED17"],
    )

    base = com.merge(rec, left_on="code_commune_insee", right_on="CODGEO")
    base = base.merge(rev, on="CODGEO")
    base = base[base.CODGEO.str.slice(0, 2) != "97"]

    base = add_distances(base, inside=False)

    return base
