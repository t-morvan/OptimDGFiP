"""
Fonctions pour pré-traiter et lire les données
"""

from importlib import resources
from typing import Optional

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

from dgfip import paths


def get_structures(crs: Optional[str] = None):
    """
    Retourne les structures DFGIP

    Args:
        crs: conversion dans le référentiel donné

    Returns:
        geodataframe des structures
    """

    with resources.path("dgfip.data", paths.STRUCTURES) as file:
        structures = pd.read_csv(file, sep=";")

    # ne garde que la France métropolitaine et les structures géocodées
    geo_struct = structures[
        structures.geocodage.str.contains(",", na=False)
        & (structures["DEPARTEMENT"].str.len() == 2)
    ]
    geo_struct = geo_struct.assign(geometry=geo_struct.geocodage.apply(extract_coord))
    geo_struct = gpd.GeoDataFrame(geo_struct, crs="4326")

    if crs is not None:
        geo_struct = geo_struct.to_crs(crs)

    return geo_struct


def get_qpv() -> gpd.GeoDataFrame:
    """
    Retourne la base de données des QPV

    Returns:
        geodataframe des qpv
    """

    fs = resources.files("dgfip.data")
    qpv = gpd.read_file(fs.joinpath(paths.QPV), crs="2154")

    return qpv


def get_iris() -> gpd.GeoDataFrame:
    """
    Retourne les informations démographiques du recensement à l'IRIS

    Returns:
        geodataframe des iris
    """

    fs = resources.files("dgfip.data")
    iris = gpd.read_file(fs.joinpath(paths.IRIS))
    rec = pd.read_csv(
        fs.joinpath(paths.RECENSEMENT),
        sep=";",
        dtype={"IRIS": str, "COM": str, "LAB_IRIS": str},
    )

    # convert to str before merging
    rec["IRIS"] = rec["IRIS"].str.ljust(9, fillchar="0")

    iris = iris.drop(columns="IRIS")
    iris_enrichi = iris.merge(rec, left_on="CODE_IRIS", right_on="IRIS")

    return iris_enrichi


def get_com() -> gpd.GeoDataFrame:
    """
    Retourne les communes enrichies des informations du recensement et de Filosofi

    Returns:
        geodataframe des communes
    """

    fs = resources.files("dgfip.data")
    com = gpd.read_file(fs.joinpath(paths.COM))
    rec = pd.read_csv(
        fs.joinpath(paths.RECENSEMENT_COM), sep=";", dtype={"CODGEO": str}
    )
    rev = pd.read_csv(
        fs.joinpath(paths.REVENUS_COM),
        sep=";",
        dtype={"CODGEO": str},
        usecols=["CODGEO", "MED17"],
    )

    base = com.merge(rec, left_on="code_commune_insee", right_on="CODGEO")
    base = base.merge(rev, on="CODGEO")
    base = base[base.CODGEO.str.slice(0, 2) != "97"]

    return base


def extract_coord(coords: str) -> Point:
    """
    Parsing des coordonnées

    Args:
        coords: coordonnées au format lon,lat

    Returns:
        Point au format Shapely
    """
    lon, lat = coords.split(",")
    return Point(float(lat), float(lon))


def get_dep(crs: Optional[bool] = None) -> gpd.GeoDataFrame:
    """
    Retourne le contour des départements

    Args:
        crs: si fourni, convertion dans le référentiel donné

    Returns:
        geodataframe des départements
    """

    with resources.path("dgfip.data", paths.DEP) as file:
        dep = gpd.read_file(file, crs="4236")

    if crs is not None:
        dep = dep.to_crs(crs)
    return dep


def get_pop_dep() -> pd.DataFrame:
    """
    Retourne la population par département

    Returns:
        population par département
    """

    fs = resources.files("dgfip.data")
    pop = pd.read_csv(fs.joinpath(paths.POP_DEP), sep=";")

    return pop
