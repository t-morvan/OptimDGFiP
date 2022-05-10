"""
Fonctions pour traiter les Quartiers Politique de la Ville (QPV)
"""

import geopandas as gpd
from dgfip import paths
from dgfip.structures import add_distances


def get_qpv(compute_distance: bool = True) -> gpd.GeoDataFrame:
    """
    Retourne la base de données des QPV

    :arg compute_distance: si vrai, enrichit la base des distances aux structures DGFIP
    """

    qpv = gpd.read_file(f"../data/{paths.QPV}", crs="2154")
    if compute_distance:
        qpv = add_distances(qpv)
    return qpv
